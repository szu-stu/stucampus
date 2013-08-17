/**
 * JavaScript Framework of StuCampus
 * 
 * @author: Developer Team of StuCampus,
 * 			Shenzhen University
 * 
 * 			TonySeek<tonyseek@gmail.com>
 */
(function(window, $) {	
	var StuCampus = {};
	
	// 初始化全站统一元素
	StuCampus.elementInit = function() {
		$('body').prepend($('<div id="message-box"></div>')); // 信息框容器
	};
	
	// 全站统一信息提示框
	StuCampus._messagebox = function(message, timeout, specialClass) {
		var entity = $('<div class="message-content"></div>')
			.hide()
			.append($('<span class="message-text"></span>').append(message))
			.append($('<a href="javascript:void(0);" class="button message-close-btn">关闭</a>'))
			.addClass(specialClass);
		
		$('#message-box').append(entity);
		
		entity.fadeIn(500);
		
		if (timeout > 0) {
			setTimeout(function(){
				entity.fadeOut(500, function(){
					$(this).remove();
				});
			}, timeout);
		}
		
		entity.children('a.message-close-btn').click(function(){
			entity.fadeOut(500, function(){
				$(this).remove();
			});
		});
	};
	StuCampus.notice = function(message, timeout) { this._messagebox(message, timeout, 'notice'); };
	StuCampus.alert  = function(message, timeout) { this._messagebox(message, timeout, 'alert');  };
	StuCampus.error  = function(message, timeout) { this._messagebox(message, timeout, 'error'); };
	
	// 用户登录
	StuCampus.signIn = function(email, password, token, success)
	{
		if (typeof success == 'undefined') {
			success = function(response){
				if (response.success) {
					// 如果有来源地址则跳转，否则给出提示并刷新页面
					if (document.referrer != '' && (document.referrer != document.location)) {
						document.location = document.referrer;
					} else {
						StuCampus.notice('登录成功', 2000);
						setTimeout(function(){
							document.location.reload();
						}, 2050);
					}
				} else {
					StuCampus.alert(response.message.join('；'), 3500);
				}
				return false;
			};
		}
		$.ajax({
			url: '/account/signin',
			type: 'post',
			cache: false,
			data: {email:email, password:password, token:token},
			success: success,
			error: function() {
				StuCampus.error('登录过程中发生了错误，我们对此给您引起的不便非常抱歉。希望您能告知我们，让我们解决这个问题。');
			}
		});
	};
	
	// 用户注销
	StuCampus.signOut = function(success) {
		if (typeof success == 'undefined') {
			success = function(){ location.reload();};
		}
		$.ajax({url: '/account/signin', type: 'delete', success:success });
	};
		
	window.StuCampus = window.$S = StuCampus;
})(window, jQuery);

/**
 * 助手工具包
 */
(function($, $S){
	if (typeof $S.Utils == 'undefined') { $S.Utils = {}; }
	
	/**
	 * 循环游标器
	 * @param length
	 */
	$S.Utils.LoopCursor = function(start, end, step){
		if (typeof end == 'undefined') { end = start; start = 0; }
		if (typeof step == 'undefined') { step = 1; }
		
		var front = (step > 0 && start < end);
		var back = (step < 0 && start > end);
		if (!front && !back) {
			throw new Error("invalid arguments");
		}
		
		this.start = start; // 开始
		this.end = end; // 结束
		this.step = step; // 步进
		this.current = null; // 当前游标
	};
	// 获取当前游标并步进
	$S.Utils.LoopCursor.prototype.get = function() {
		if (this.current === null) {
			this.current = this.start - this.step;
		}
		
		this.current += this.step; // 推进
		
		var overflowUp = (this.step > 0 && this.current > this.end);
		var overflowDown = (this.step < 0 && this.current < this.end);
		
		if (overflowUp || overflowDown) {
			this.current = this.start; // 溢出后重置
		}
		
		return this.current;
	};
	$S.Utils.LoopCursor.prototype.setCurrent = function(current) { 
		this.current = current; 
	};
	
})(jQuery, StuCampus);

/**
 * 主干业务
 */
(function($, $S){
	$S.User = function(id, screenName, avatar, school) {
		this.id = id;
		this.name = screenName;
		this.avatar = avatar;
		this.school = school;
	};
	
})(jQuery, StuCampus);

$(function(){
	// 初始化元素
	$S.elementInit();
});


//验证码js
function reloadCaptcha(imgObj) {
	$(imgObj).fadeOut('fast', function(){
		var datenow = new Date();
		$(this).attr('src', '/captcha/?ver=' + datenow.getMilliseconds()).delay(200).fadeIn('slow');
    });
}

// 阻止中国电信、中国联通的页面劫持
$(function(){
    if (top !== self) {
        if (top.location == self.location) {
            alert("您的页面可能遭到了网关或运营商的劫持");
        } else {
            top.location = self.location;
        }
    }
});
