;(function($)
{
	$("#register_form_submit_btn").click(function(){
		$.ajax({
			type:"post",
			url:"/dreamer/joinus",
			dataType:"json",
			data:$("#register_form").serialize(),
			success:function(data){
				console.log("success2");
				if(data.status=="success"){
					$("#register_form").html('<p>'+data.name+'同学，你已经<span class="success_msg">成功报名</span>学子天地，期待您的加入</p>');
				}
				else
				{
					$("#error_msg").text(data.messages);
				}
			},
			error: function(data, status, e){
            	alert("出现错误，请联系qq：649743466");
            	console.log(data);
            },
		});
	});


})(jQuery);