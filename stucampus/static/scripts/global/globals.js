var isChrome = window.navigator.userAgent.indexOf("Chrome") !== -1;
if(isChrome) {
    $("head").append('<script type="text/javascript" src="scripts/chromeCookie.js"></script>');
    var nownavid = localStorage.getItem('navnowid');
} 
else{
    $("head").append('<script type="text/javascript" src="scripts/cookie.js"></script>');
        var nownavid = GetCookie('navnowid');
}
window.onresize = function(){
    w = document.body.clientWidth;
    resized(w);
}

function resized(windowswidth){
    if(windowswidth<=767){
        fontsize= windowswidth/750*30 ;
    }
    else if(windowswidth>=768&&windowswidth<=1366){
        fontsize = windowswidth/1366*30;
    } 
    else if(windowswidth>1366){
        fontsize = 30;
    }
    $("html").css("font-size",fontsize+"px");
}
function navcome(navid){
    nownav = $(".now");
    if(navid==nownavid){
        nownav.css("left",navid*4.0+"rem");
        return false;
    }
    for(i=0;i<5;i++){
        $("#nav"+i).removeClass("nav-active");
    }
    if(navid==0){
        nownav.css("left",navid*4.0+"rem");
        nownav.show();
        $("#nav"+navid).addClass("nav-active");
        if(isChrome){
            SetLocalStorage('navnowid',navid)
        }else{
            SetCookie('navnowid',navid);
        }
        setTimeout(function(){
            window.location.href = "/index.html";
        },500);
    }
    else if(navid==1){
        nownav.css("left",navid*4.0+"rem");
        nownav.show();
        $("#nav"+navid).addClass("nav-active");
        if(isChrome){
            SetLocalStorage('navnowid',navid)
        }else{
            SetCookie('navnowid',navid);
        }
        setTimeout(function(){
            window.location.href = "/artical.html";
        },500);
    }
    else if(navid==2){
        nownav.css("left",navid*4.0+"rem");
        nownav.show();
        $("#nav"+navid).addClass("nav-active");
        if(isChrome){
            SetLocalStorage('navnowid',navid)
        }else{
            SetCookie('navnowid',navid);
        }
        setTimeout(function(){
            window.location.href = "http://stu.szu.edu.cn/activity/";
        },500);
    }
    else if(navid==3){
        nownav.css("left",navid*4.0+"rem");
        nownav.show();
        $("#nav"+navid).addClass("nav-active");
        if(isChrome){
            SetLocalStorage('navnowid',navid)
        }else{
            SetCookie('navnowid',navid);
        }
        setTimeout(function(){
            window.location.href = "http://stu.szu.edu.cn/articles/photography/";
        },500);
    }
    else if(navid==4){
        nownav.css("left",navid*4.0+"rem");
        nownav.show();
        $("#nav"+navid).addClass("nav-active");
        if(isChrome){
            SetLocalStorage('navnowid',navid)
        }else{
            SetCookie('navnowid',navid);
        }
        setTimeout(function(){
            window.location.href = "http://stu.szu.edu.cn:8080/";
        },500);
    }
}