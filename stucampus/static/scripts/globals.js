window.onresize = function(){
    w = document.body.clientWidth;
    resized(w);
}
$(function(){
    w = document.body.clientWidth;
    var nowurl = window.location.pathname;
    $('.autoadapt > ul > li > a').each(function(){
        if($(this).attr('tarurl').search('^'+nowurl,'i')==0){
            nownavid = $(this).attr('id');
            return false;
        }
        else{
            nownavid = null;
        }
    });
    navcome(nownavid);
    resized(w);
});

function resized(windowswidth){
    if(windowswidth<=767){
        fontsize= windowswidth/750*30 ;
    }
    else if(windowswidth>=768&&windowswidth<960){
        fontsize = windowswidth/1366*30;
    } 
    else if(windowswidth>=960){
        fontsize = 30;
    }
    $("html").css("font-size",fontsize+"px");
}
var navcome = function(navid){
    nownav = $(".now");
    for(i=0;i<5;i++){
        $("#nav"+i).removeClass("nav-active");
    }
    if (navid==null) {
        nownav.hide();
        return false;
    };
    if(navid==nownavid){
        nownav.show();
        nownav.css("left",navid[3]*4.0+"rem");
        $("#"+navid).addClass("nav-active");
        return false;
    }
    if(navid==0){
        nownav.css("left",navid*4.0+"rem");
        nownav.show();
        $("#"+navid).addClass("nav-active");
        setTimeout(function(){
            window.location.href = "/";
        },500);
    }
    else if(navid==1){
        nownav.css("left",navid*4.0+"rem");
        nownav.show();
        $("#"+navid).addClass("nav-active");
        setTimeout(function(){
            window.location.href = "/lecture/";
        },500);
    }
    else if(navid==2){
        nownav.css("left",navid*4.0+"rem");
        nownav.show();
        $("#"+navid).addClass("nav-active");
        setTimeout(function(){
            window.location.href = "/activity/";
        },500);
    }
    else if(navid==3){
        nownav.css("left",navid*4.0+"rem");
        nownav.show();
        $("#"+navid).addClass("nav-active");
        setTimeout(function(){
            window.location.href = "/articles/photography/";
        },500);
    }
    else if("#"+navid==4){
        nownav.css("left",navid*4.0+"rem");
        nownav.show();
        $(navid).addClass("nav-active");
        setTimeout(function(){
            window.location.href = "http://stu.szu.edu.cn:8080/";
        },500);
    }
}