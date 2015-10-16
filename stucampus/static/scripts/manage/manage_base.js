//屏幕高度适应
function heightCtrol () {
    var heightNeed=document.documentElement.clientHeight-document.getElementById('header').offsetHeight-document.getElementById('footer').offsetHeight;
    var content=document.getElementById('layout_content');
    var menu=document.getElementById('layout_left');
    if (heightNeed>=menu.offsetHeight) {
        content.style.minHeight=heightNeed+"px";
        menu.style.position="fixed";
        menu.style.top="80px";
        //document.getElementById('menu_box').style.height=content.offsetHeight+"px";
    }
    else
    {
        content.style.minHeight=menu.offsetHeight+"px";
        menu.style.position="absolute";
        menu.style.top="0px";
        //document.getElementById('menu_box').style.height=content.offsetHeight+"px";
    }
}
