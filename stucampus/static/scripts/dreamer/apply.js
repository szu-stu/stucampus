 function textCounter(field, countfield, limit)
 {   
 	if (field.value.length > limit)    
 		field.value = field.value.substring(0, limit);  
 	else 
 		countfield.value = limit - field.value.length;  
 }     

 function Judge()
 {
 	$(document).ready(function(){
 		flag = 0
 		var data1 = document.getElementById("name").value.replace(/(^\s*)|(\s*$)/g,'');
 		var data2 = document.getElementById('number').value.replace(/(^\s*)|(\s*$)/g,'');
 		var data3 = document.getElementById('college').value.replace(/(^\s*)|(\s*$)/g,'');
 		var data4 = document.getElementById('tel').value.replace(/(^\s*)|(\s*$)/g,'');
 		var data5 = document.getElementById('sex').value.replace(/(^\s*)|(\s*$)/g,'');
 		var data6 = document.getElementById('hobby').value.replace(/(^\s*)|(\s*$)/g,'');
 		if (data1&&data2&&data3&&data4&&data5&&data6&&data1!="姓名"&&data2!="学号"&&data3!="学院"&&data4!="手机号码"&&data5!="性别")
 			flag = 1;
 	})
 }


 function notify()
 {
 	if(flag==0)
 	{
 		alert("请填写完整所有信息，谢谢");
 	}
 }
 $(document).ready
 (
 	function()
 	{
 		$(".flip").click
 		(
 			function()
 			{
 				$(".panel").slideToggle("slow");
 			}
 			);
 	}
 	);