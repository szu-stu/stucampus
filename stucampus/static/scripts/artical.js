var logoclicktime = 0;
$(function(){
    var biaogan = parseInt($(".artical-header").css("height"))*2/5;
    window.onscroll = function scrolls(){
        console.log(biaogan);
        if(document.body.clientWidth>750){
            return false;
        }
        var scrollTop = document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;
        if(scrollTop>=biaogan){
            $(".artical-header").addClass("up");
            $(".blur").hide();
            $(".artical-title").addClass("artical-title-up");
            $(".artical-main").addClass("main-up");
            $(".artical-cover").hide();
        }
        else if(scrollTop<biaogan){
            $(".artical-header").removeClass("up");
            $(".blur").show();
            $(".artical-title").removeClass("artical-title-up");
            $(".artical-main").removeClass("main-up");
            $(".artical-cover").show();
        }
    }
    $(".now").hide();
    $("#nav0").removeClass("nav-active");
    setTimeout(function(){
        $(".fixed-logo").addClass("scale1");
    },500);
    $("#backTop").click(function() {
        $('html, body').animate({
            scrollTop: '0px'
        }, 800);
        $(".fixed-logo").click();
    });
    w = document.body.clientWidth;
    resized(w);
    navcome(nownavid);
    $(".fixed-logo").bind('click',function(){showtools();});
    $(".comment").bind('click',function(){showcommenttools();});
    $("#discuss").bind('click',function(){showcommenttools();showtools();});
    $(".share").bind('click',function(){showsharetools();});
    $("#share").bind('click',function(){showsharetools();});
    $(".backarticalfoot").bind('click',function(){
        $(".add-comment").removeClass("appear");
        $(".sharebox").removeClass("appear");
        $(".fixed-logo").addClass('scale1');
    });
    $(".addcomment").focus(function(){setTimeout(function(){$(".fixed-logo").removeClass('scale1');},500);});
    $(".addcomment").blur(function(){$(".fixed-logo").addClass('scale1');});
});
function showtools(){
    logoclicktime += 1;
    if(logoclicktime%2 != 0){
        $(".btn").addClass("scale1");
        setTimeout(function(){
            $("#backTop").css("bottom","5.86667rem");
            $("#share").css("bottom","9.6rem");
            $("#discuss").css("bottom","13.33333rem");
            $("#like").css("bottom","17.06667rem");
        },300);
    }
    else if(logoclicktime%2 == 0){
        $("#backTop").css("bottom","1.6rem");
        $("#share").css("bottom","1.6rem");
        $("#discuss").css("bottom","1.6rem");
        $("#like").css("bottom","1.6rem");
        setTimeout(function(){
            $(".btn").removeClass("scale1");
        },500);
    }
}
function showcommenttools(){
    $(".sharebox").show();
    $(".add-comment").show();
    $(".add-comment-cover").show();
    setTimeout(function(){
        $(".add-comment").addClass("appear");
        $(".add-comment-cover").addClass("appear");
        $(".addcomment").focus();
        $(".sharebox").removeClass("appear");
    },100);
}
function showsharetools(){
    $(".sharebox").show();
    $(".add-comment").show();
    setTimeout(function(){
        $(".sharebox").addClass("appear");
        $("body,html").animate({ 
            scrollTop:$(".sharebox").offset().top+100 //让body的scrollTop等于pos的top，就实现了滚动 
        },0); 
        $(".add-comment").removeClass("appear");
    },100);
}
function showIdentityBox(){
    var message = $(".addcomment").val();
    if($.trim(message)==""){
        StuCampus.alert("你还没有输入内容呢");
        return false;
    }
    $(".background").show();
    $(".background").bind('click',function(){
        $(".background").hide();
        $(".ds-dialog-inner").hide();
        $(".ds-dialog-inner > input").val("");
    });
    StuCampus.alert("点击灰区关闭tips",5000);
    $(".ds-dialog-inner").show();
}
$(document).ready(function(){
    var total = $(".comments").length;
    for(var i = 0 ; i < total ;++i)
    {
        var profindex =Math.round(Math.random()*3);
        var newstr = "/static/images/articles/avatar"+profindex+".jpg";
        $(".comments:eq("+i+")").find(".avatar").attr("src",newstr);
    }
})