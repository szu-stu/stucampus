$(function(){
	$('#sign_in-form').submit(function(){
		$.ajax({
			url: '/account/signin',
			type: 'post',
			dataType: 'json',
			data: $(this).serialize(),
			success: function(response){
				if(response.success){
					// 如果有来源地址则跳转，否则给出提示并刷新页面
					if (document.referrer != '' && (document.referrer != document.location)) {
						jump_url = document.referrer;
					} else {
						jump_url = '/'
					}
					$S.notice('登录成功', 2000);
					setTimeout(function(){
						document.location = jump_url;
					}, 2050);
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

	$('#sign_up-btn').click(function(){
		document.location = '/account/signup';
	});

	// 登录框就不要多此一举出现了
	$('#signer-box').remove();
});