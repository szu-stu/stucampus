$(document).ready(function(){
    var day = new Date().getDay();
    if(day == 0) day = 7;
    var td_list = document.getElementsByTagName('td');
    for(var i=0; i<td_list.length; i++)
    {
        if(td_list[i].className == "day"+day)
        {
            td_list[i].style.backgroundColor = "#f2a0a1";
            td_list[i].style.color="#d3381c";
        }
        else if(td_list[i].className < "day"+day)
        {
            td_list[i].style.backgroundColor = "#f7f7f7";
            td_list[i].style.color = "#e5e5e5";
        }
    }
    var div_list = document.getElementById('main-container').getElementsByTagName('div');
    for(var j=0;j<div_list.length;j++)
    {
        if(div_list[j].parentNode.className<"day"+day)
            div_list[j].style.color="#e5e5e5";
    }
})
