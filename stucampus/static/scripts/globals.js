window.onresize = function(){
    var w = document.body.clientWidth;
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
    $(".sidebar-main")
       .bind('touchstart', navtouchstart)
       .bind('touchend',navtouchend);
});

function resized(windowswidth){
    if(windowswidth<=767){
        fontsize= windowswidth/750*30 ;
    }
    else if(windowswidth>=768&&windowswidth<980){
        fontsize = windowswidth/980*30;
    } 
    else if(windowswidth>=980){
        fontsize = 30;
    }
    $("html").css("font-size",fontsize+"px");
}
var navcome = function(navid){
    nownav = $(".now");
    for(i=0;i<6;i++){
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
    if(navid<=5&&navid>=0){
        nownav.css("left",navid*4.0+"rem");
        nownav.show();
        $("#nav"+navid).addClass("nav-active");
    }
    else{
        return false;
    }
    setTimeout(function(){
        window.location.href = $("#nav"+navid).attr("tarurl");
    },500);
}
function sidebaropen(){
    $(".fixed-logo").css("transform","scale(0)");
    $(".header-nav").show();
    setTimeout(function(){
        $(".header-nav").addClass("sidebarout");
        $(".call-back").show();
    },100);
    return false;
}
function sidebarclose(){
    setTimeout(function(){
        $(".fixed-logo").css("transform","scale(1)");
    },500);
    $(".header-nav").removeClass("sidebarout");
    $(".call-back").hide();
    setTimeout(function(){
        $(".header-nav").hide();
    },500);
    return false;
}

function navtouchstart(event){
    touch = event.originalEvent.targetTouches[0];
    firstPos = {
        x : Number(touch.pageX),
        y : Number(touch.pageY)
    };
};
function navtouchend(event){
    touch = event.originalEvent.changedTouches[0];
    lastPos = {
        x : Number(touch.pageX),
        y : Number(touch.pageY)
    };
    if(lastPos["x"]<firstPos["x"]){
        sidebarclose();
    }
};