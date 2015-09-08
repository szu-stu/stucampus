
$(document).ready(function()
{
	$(".department_img li").bind("click",function()
	{
		var department=$(this).text().trim();
		$(".department_img li span").hide("fast");
		$(".department_infor p").hide("fast");

		if(department=="技术部")
		{

			$("span", this).fadeIn(1000);
			$(".department_infor .jishu").fadeIn(1000,function() {

			});

		}
		else if(department=="行政部")
		{

			$("span", this).fadeIn(1000,function() {

			});
			$(".department_infor .xingzheng").fadeIn(1000);


		}
		else if(department=="设计部")
		{

			$("span", this).fadeIn(1000);
			$(".department_infor .sheji").fadeIn(1000);


		}
		else if(department=="运营部")
		{

			$("span", this).fadeIn(1000);
			$(".department_infor .yunying").fadeIn(1000);


		}
		else if(department=="采编部")
		{

			$("span", this).fadeIn(1000);
			$(".department_infor .caibian").fadeIn(1000);


		}

	})

})

function checkLen(obj)  
{ 
    var maxChars = 500;//最多字符数 
    if (obj.value.length > maxChars) 
    	obj.value = obj.value.substring(0,maxChars); 
    var curr = obj.value.length; 
    document.getElementById("count").innerHTML = curr.toString(); 
} 
function Judge()
{
	$(document).ready(function(){
		flag = 0
		var data1 = document.getElementById("name").value.replace(/(^\s*)|(\s*$)/g,'');
		var data2 = document.getElementById('stu_ID').value.replace(/(^\s*)|(\s*$)/g,'');
		var data3 = document.getElementById('college').value.replace(/(^\s*)|(\s*$)/g,'');
		var data4 = document.getElementById('tel').value.replace(/(^\s*)|(\s*$)/g,'');
		var data5 = document.getElementById('gender').value.replace(/(^\s*)|(\s*$)/g,'');
		var data6 = document.getElementById('self_intro').value.replace(/(^\s*)|(\s*$)/g,'');
		if (data1&&data2&&data3&&data4&&data5&&data6&&data1!="姓名"&&data2!="学号"&&data3!="学院"&&data4!="手机号码"&&data5!="性别")
		{
			flag = 1;
		}


	})
}


function notify()
{
	if(flag==0)
	{
		alert("请填写完整所有信息，谢谢");
	}
}

