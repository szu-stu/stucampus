 function textCounter(field, countfield, limit)
 {   
 	if (field.value.length > limit)    
 		field.value = field.value.substring(0, limit);  
 	else 
 		countfield.value = limit - field.value.length;  
 }     
 $(':submit').click(function(event)
 {
 	var json_data = global_json_data;
 	event.preventDefault();
 });
 $(document).ready(function()
 {
 	$("#number").blur(function()
 	{
 		$number=$("#number").value.length;
 		if ($number!=11) 
 		{
 			alert("学号有误");
 		}
 	});
 	$("#tel").blur(function()
 	{
 		$tel=$("#tel").value.length;
 		if ($tel!=11) 
 		{
 			alert("号码有误");
 		}
 	});
 });
 $(":submit").click(Judge(event));

 function Judge(event)
 {
 	
 	var data1 = $("#name").value;
 	var data2 = $('number').value;
 	var data3 = $('college').value;
 	var data4 = $('tel').value;
 	var data5 = $('sex').value;
 	var data6 = $('hobby').value;
 	if(isNaN(data2))
 	{
 		alert("同学，你填写的学号有误");
 	}
 	else{
 		if(data2.value.length=6)
 		{
 			alert("同学，请填写学号，而不是卡号哦");
 		}
 		else if(data2.value.length<10)
 		{
 			alert("同学，你填写的学号有误");
 		}

 	}
 	if(isNaN(data4))
 	{
 		alert("同学，你填写的手机号有误");
 	}
 	else 
 	{
 		if(data4.value.length<11)
 		{
 			alert("同学，你填写的手机号有误");
 		}


 	}

 	if (data1&&data2&&data3&&data4&&data5&&data6&&data1!="姓名"&&data2!="学号"&&data3!="学院"&&data4!="手机号码"&&data5!="性别")
 	{
 		alert("请填写完整所有信息，谢谢");
 	}
 	
 }


