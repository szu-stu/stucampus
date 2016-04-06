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
        $("#nav"+navid).addClass("nav-active");
    }
    else if(navid==1){
        nownav.css("left",navid*4.0+"rem");
        nownav.show();
        $("#nav"+navid).addClass("nav-active");
    }
    else if(navid==2){
        nownav.css("left",navid*4.0+"rem");
        nownav.show();
        $("#nav"+navid).addClass("nav-active");
    }
    else if(navid==3){
        nownav.css("left",navid*4.0+"rem");
        nownav.show();
        $("#nav"+navid).addClass("nav-active");
    }
    else if(navid==4){
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
    $(".sidebar").show();
    setTimeout(function(){
        $(".sidebar").addClass("sidebarout");
        $(".call-back").show();
    },100);
    return false;
}
function sidebarclose(){
    setTimeout(function(){
        $(".fixed-logo").css("transform","scale(1)");
    },500);
    $(".sidebar").removeClass("sidebarout");
    $(".call-back").hide();
    setTimeout(function(){
        $(".sidebar").hide();
    },500);
    return false;
}