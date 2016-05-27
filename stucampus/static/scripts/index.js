var fontsize;
var now = 0;
var logoclicktime = 0;
$(function(){
    var gallery = $('.slide-container').swiper({
        slidesPerView:'auto',
        watchActiveIndex: true,
        centeredSlides: true,  //若为真，那么活动块会居中，而非默认状态下的居左
        pagination:'.swiper-pagination',
        paginationClickable: true, //当单击指示器时会执行过渡动画到目标slide
        resizeReInit: true,
        keyboardControl: true, //能使用键盘左右方向键滑动
        grabCursor: true,  //光标在Swiper上时成手掌状
        loop: true,
        autoplay: 4000,
        autoplayDisableOnInteraction: false
    })
    $(".swiper-pagination > span").get(parseInt($(".swiper-pagination > span").length/2)).click();
})

window.onload = function(){
    $(".sidebar").hide();
    setTimeout(function(){
        $(".fixed-logo").css("transform","scale(1)");
    },500);
    var w = document.body.clientWidth;
    resized(w);
    $(".fixed-logo").bind('click',function(){hiddenthings();});
};

function hiddenthings(){
    logoclicktime += 1;
    if(logoclicktime<=5){
        $('html, body').animate({
            scrollTop: '0px'
        }, 800);
    }
    if(logoclicktime==6){
        $(".fixed-logo").css("transform","scale(4)");
        $(".fixed-logo").css("opacity","0");
        setTimeout(function(){
            window.location.href = "/manage/index";
        },500);
    }
};
