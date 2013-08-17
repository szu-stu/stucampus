$(function(){
	$('#sign_up-form').submit(function(){
		$.ajax({
			url: '/account/signup',
			type: 'post',
			dataType: 'json',
			data: $(this).serialize(),
			success: function(response){
				if(response.success){
					// 如果有来源地址则跳转，否则给出提示并刷新页面
					if (document.referrer != '' && (document.referrer != document.location)) {
						document.location = document.referrer;
					} else {
						$S.notice('注册成功', 2000);
						setTimeout(function(){
							document.location = '/account/signin';
						}, 2050);
					}
				}
				else{
					$S.alert(response.messages.join('；'), 3500);
				}
			},
			error: function() {
				$S.error('程序发生错误，请联系管理员！');
			}
		});
		return false;
	});
});