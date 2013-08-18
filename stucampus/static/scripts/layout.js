(function($, $S){
	if (typeof $S.frontLayout == 'undefined') {
		$S.frontLayout = {};
	}
	
	// 刷新登录情况
	$S.frontLayout.ajaxReflushSign = function() {
		$.ajax({
			url: '/user/me',
			data: {type:'html_dl'},
			type: 'get',
			dataType: 'html',
			cache: false,
			success: function(response) {
				$('dl#signer-box').html($(response).html());
				$S.frontLayout.signbox.bind(); // 重新绑定
			}
		});
	};
	
	// 登录
	$S.frontLayout.ajaxSignIn = function(email, password, token) {
		$S.signIn(email, password, token, function(result){
			if (result.success) {
				$S.frontLayout.ajaxReflushSign();
				document.location.reload();
			} else {
				StuCampus.error(result.message.join('、'), 3000);
			}
		});
	};
	
	$S.frontLayout.ajaxSignOut = function() {
		$S.signOut(function() {
			$S.frontLayout.ajaxReflushSign();
			document.location.reload();
		});
	};
	
	// 登录框
	$S.frontLayout.signbox = new (function(){
		this.hasOpened = false;
		this.elements = null;
		
		
		this.open = function() {
			var self = this;
			// 如果已打开则忽略
			if (this.hasOpened) return; 
			// 修改样式
			this.elements.addClass('pushed'); 
			// 绑定消失事件
			$('body').click(function(event) {
				self.close();
				$(this).unbind('click');
				event.stopPropagation();
			});
			// 阻止冒泡
			$('dd#signer-expand').click(function(event){
				event.stopPropagation();
			});
			this.hasOpened = true;
		};
		this.close = function() {
			// 如果未打开则忽略
			if (!this.hasOpened) return;
			// 修改样式
			this.elements.removeClass('pushed');
			this.hasOpened = false;
		};
		this.bind = function() {
			var self = this;
			$('a#signer-more').click(function(event) {
				self.open();
				event.stopPropagation();
			});
			// 登录动作
			$('form#signin-form').submit(function() {
				try {
					var email = $('#signin-email').val();
					var password = $('#signin-pwd').val();
					var token = $('#signin-token').val(); // TODO: 令牌
					$S.frontLayout.ajaxSignIn(email, password, token);
				} catch (e) {
					console.log(e);
					throw e;
				} finally {
					return false;
				}
			});
			// 注销动作
			$('#signout-btn').click(function(){
				$S.frontLayout.ajaxSignOut();
			});
			this.elements = $('a#signer-more, dd#signer-expand, .signer-head');
			this.hasOpened = false;
		};
	})();
})(jQuery, StuCampus);

// 登录框
$(function(){

	$S.frontLayout.signbox.bind();
	
	window.signbox = $S.frontLayout.signbox;
});
