# -*- coding: utf-8 -*-
import logging
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from models import *
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.db.models import Count
from forms import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
import json
from django.core import serializers
from django.http import JsonResponse

logger = logging.getLogger('blog.views')

# Create your views here.

# set global settings
def global_settings(request):
    # 全局配置
    SITE_NAME = settings.SITE_NAME
    SITE_URL = settings.SITE_URL
    SITE_DESC = settings.SITE_DESC
    SITE_WEIBO = settings.SITE_WEIBO
    SITE_WEIXIN = settings.SITE_WEIXIN
    PRO_RSS = settings.PRO_RSS
    PRO_EMAIL = settings.PRO_EMAIL
    MEDIA_URL = settings.MEDIA_URL
    # 导航分类
    category_list = Category.objects.all()[:6]
    # 归档目录
    try:
        # archive list
        archive_list = Article.objects.distinct_date()
    except Exception as e:
        print e
        logger.error(e)
    # 广告
    ad_list = Ad.objects.all()[:4]
    ad_list_1 = ad_list[0]
    ad_list_2 = ad_list[1]
    ad_list_3 = ad_list[2]
    ad_list_4 = ad_list[3]
    # print ad_list_2.description
    # 浏览排名
    click_count_list = Article.objects.values('title','id').order_by('-click_count')
    # 评论排名
    comment_count_list = Comment.objects.values('article').annotate(commentcount=Count('article')).order_by('-commentcount')
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]
    # 站长推荐
    recomend_list = Article.objects.values('title','id').order_by('-is_recommend')
    # 标签云
    tag_list = Tag.objects.all()
    # 友情链接
    link_list = Links.objects.all()[:6]
    return locals()


def index(request):
    try:
        article_list = getpage(request, Article.objects.all())
    except Exception as e:
        logger.error(e)
    return render(request, 'index.html', locals())

def archive(request):
    try:
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        # article_list = Article.objects.filter(date_publish__year=year,date_publish__month=month)
        article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)
        article_list = getpage(request,article_list)
    except Exception as e:
        logger.error(e)

    return render(request, 'archive.html', locals())

def tag(request):
    try:
        tagid = request.GET.get('tag', None)
        article_list = Article.objects.filter(tag=tagid)
        tag = Tag.objects.get(id=tagid)
        article_list = getpage(request,article_list)
    except Exception as e:
        logger.error(e)

    return render(request, 'tag.html', locals())

def category(request):
    try:
        cid = request.GET.get('cid', None)
        article_list = Article.objects.filter(category=cid)
        category = Category.objects.get(id=cid)
        article_list = getpage(request,article_list)
    except Exception as e:
        logger.error(e)

    return render(request, 'category.html', locals())

def article(request):
    try:
        articleid = request.GET.get('articleid', None)
        article = Article.objects.get(id=articleid)
    except Article.DoesNotExist as e:
        return render(request, 'failure.html', {'reason': '没找到对应文章哦'})

    # 评论表单
    comment_form = CommentForm({'author': request.user.username,
                                'email': request.user.email,
                                'url': request.user.url,
                                'article': articleid} if request.user.is_authenticated() else{'article': articleid})
    # 获取评论信息
    comments = Comment.objects.filter(article=articleid).order_by('id')
    comment_list=[]
    for comment in comments:
        for item in comment_list:
            if not hasattr(item, 'children_comment'):
                setattr(item, 'children_comment', [])
            if comment.pid == item:
                item.children_comment.append(comment)
                break
        if comment.pid is None:
            comment_list.append(comment)
    comment_count = comment_list.__len__()
    # comment_list = comment_list.__reversed__()
    # comment_list = getpage(request, comment_list)
    return render(request, 'article.html', locals())

# def comment_post(request):
#     try:
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             # 获取表单信息
#             comment = Comment.objects.create(
#                 username = comment_form.cleaned_data['author'],
#                 email=comment_form.cleaned_data["email"],
#                 url=comment_form.cleaned_data["url"],
#                 content=comment_form.cleaned_data["comment"],
#                 article_id=comment_form.cleaned_data["article"],
#                 user=request.user if request.user.is_authenticated() else None
#             )
#             comment.save()
#         else:
#             return render(request, 'failure.html', {'reason': comment_form.errors})
#     except Exception as e:
#         logger.error(e)
#         print e
#     return redirect(request.META['HTTP_REFERER'])

# ajax方式实现
def comment_post(request):
    data = "hello world"
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment.objects.create(
                username=comment_form.cleaned_data['author'],
                email=comment_form.cleaned_data["email"],
                url=comment_form.cleaned_data["url"],
                content=comment_form.cleaned_data["comment"],
                article_id=comment_form.cleaned_data["article"],
                user=request.user if request.user.is_authenticated() else None
            )
            comment.save()
        else:
            render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        print e
        logger.error(e)
    # print type(comment.content)
    # print type(request.POST)

    try:
        print type(comment)
        commentorg = comment
        comment = {}

        comment['content'] = commentorg.content
        comment['username'] = commentorg.username
        comment['url'] = commentorg.url
        comment['date_publish'] = commentorg.date_publish
        comment['article_id'] = commentorg.article_id

        # comment = comment.toJSON()
        # comment = comment['content']
        # print comment
        # print type(comment)
        # print type(comment)
        # comment = comment.content
        # return HttpResponse(comment)
        # try:
        #     response = HttpResponse(json.dumps(serializers.serialize("json", comment)), content_type="application/json")
        response = JsonResponse(comment)
        # except Exception as e:
        #     print e
        # print type(response)
        # comment = comment['username']
        # print comment
        # response =  HttpResponse(json.dumps(serializers.serialize("json", comment)), content_type="application/json")
        # response =  HttpResponse(comment)
        # response =  HttpResponse(json.dumps(comment), mimetype = 'application/json')
    except Exception as e:
        print e
    return response

def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                # source_url = login_form.cleaned_data['source_url']
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                    login(request, user)
                    return redirect(request.POST.get('source_url'))
                else:
                    return render(request, 'failure.html', {'reason': '用户验证失败'})
        else:
            login_form = LoginForm()
    except Exception as e:
        print e
        logger.error(e)
    return render(request, 'login.html', locals())

def do_reg(request):
    try:
        # 注册
        if request.method == 'POST':
            reg_form=RegForm(request.POST)
            if reg_form.is_valid():
                user = User.objects.create(
                    username = reg_form.cleaned_data['username'],
                    email = reg_form.cleaned_data['email'],
                    url = reg_form.cleaned_data['url'],
                    password = make_password(reg_form.cleaned_data['password']),
                )
                user.save()
                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': '注册失败'})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())

def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logger.error(e)
        print e
    return redirect(request.META['HTTP_REFERER'])

def getpage(request,article_list):
    try:
        paginator = Paginator(article_list, 4)
        page = request.GET.get('page')
        article_list = paginator.page(page)

    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list