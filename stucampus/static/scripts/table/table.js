$(document).ready(function(){
	var day = new Date().getDay();
	if(day == 0) day = 7;
	var td_list = document.getElementsByTagName('td');
	for(var i=0; i<td_list.length; i++)
	{
		if(td_list[i].className == "day"+day)
		{
			td_list[i].style.backgroundColor = "#f2a0a1";
			if(td_list[i].className == "day"+day)
				td_list[i].style.color="#d3381c";
		}
		else if(td_list[i].className < "day"+day)
		{
			td_list[i].style.backgroundColor = "#eeeeee";
			td_list[i].style.color = "#aaaaaa";
		}
	}
})
