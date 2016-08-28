/**
 * Created by Lvzq on 2016/6/19.
 */

$(function(){
    var frm = $("#commentformid");
    // frm.submit(function ()
    $("#submit").click(function () {
        // alert("{% url 'comment_post' %}")
        $.ajax({
            cache: true,
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            // data: {name:'name', password:'password'},
            async: false,
            error: function(request){
                alert("Connection Error");
            },
            success: function(comment){
                // comment = eval("("+comment+")");
                // comment = JSON.parse(comment)
                // alert(comment.username.toString());

                photosrc=$(".avatar").attr('src')
                newcomment =
                "<li id='comment-59418'> \
                <div class='top'><a href='"+comment.url.toString()+"' rel='external nofollow' class='url'>"+comment.username.toString()+"</a><span class='time'> @ <a href='#comment-59418' title=''>"+comment.date_publish+"</a></span></div> \
                <div><img alt='' src='"+photosrc+"' class='avatar avatar-32 photo' height='32' width='32' /></div> \
                <div class='body'> \
                                <p>"+comment.content.toString()+"</p> \
                </div> \
                 </li> ";
                $(".commentlist").append(newcomment)

            }

    });

    });

});
