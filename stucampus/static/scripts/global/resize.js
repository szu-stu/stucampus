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
    if(navid==6){
        nownav.css("left",0+"rem");
        return false;
    }
    for(i=0;i<5;i++){
        $("#nav"+i).removeClass("nav-active");
    }
    if(navid==0){
        nownav.css("left",navid*4.0+"rem");
        $("#nav"+navid).addClass("nav-active");
        setTimeout(function(){
            window.location.href = "http://stu.szu.edu.cn/";
        },500);
    }
    else if(navid==1){
        nownav.css("left",navid*4.0+"rem");
        $("#nav"+navid).addClass("nav-active");
        setTimeout(function(){
            window.location.href = "http://stu.szu.edu.cn/lecture/";
        },500);
    }
    else if(navid==2){
        nownav.css("left",navid*4.0+"rem");
        $("#nav"+navid).addClass("nav-active");
        setTimeout(function(){
            window.location.href = "http://stu.szu.edu.cn/activity/";
        },500);
    }
    else if(navid==3){
        nownav.css("left",navid*4.0+"rem");
        $("#nav"+navid).addClass("nav-active");
        setTimeout(function(){
            window.location.href = "http://stu.szu.edu.cn/articles/photography/";
        },500);
    }
    else if(navid==4){
        nownav.css("left",navid*4.0+"rem");
        $("#nav"+navid).addClass("nav-active");
        setTimeout(function(){
            window.location.href = "http://stu.szu.edu.cn:8080/";
        },500);
    }
}