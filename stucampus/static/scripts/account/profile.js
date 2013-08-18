
$(function () {
	
	//生日日期插件
	$(":date").dateinput({
	format: 'yyyy-mm-dd',
	selectors: true,
	yearRange: [-40,10],
	min: -20000,  
	max: 10000
	});
	
});

$(function() {
	
	//绑定表单ajax
	var elements = $('form#changeInfor').find('input');
	$('form#changeInfor').ajaxForm({
			success: function(response) {
				var message = response.message.join("、");
				if(response.success){
					$S.notice(message);
					setTimeout(function(){
						document.location = '/user';
					}, 3000);
			}
			else {
				$S.alert(response.message.join('、') , 3000);
				elements.delay(1000).removeAttr('disabled');
			}
			},
			error: function() {
				$S.error('由于服务器错误，您的资料修改失败，对此我们十分抱歉，服务器已经记录此次错误，我们将尽快解决这个问题。');
				elements.delay(2000).removeAttr('disabled');
			}
		});
});

/*组织发布信息*/
$(function(){
	// 加载所见即所得编辑器
	$('#content').ckeditor({
		contentsCss: '/static/styles/news/editor.css',
		height: '300px',
        width:   '530px'
	});

	// 绑定表单 ajax
	var elements = $('form#infor').find('input, textarea');
	$('form#infor').ajaxForm({
		beforeSubmit: function(){
			elements.attr('disabled', 'disabled');
		},
		success: function(response){
			var message = response.message.join("、");
			if (response.success) {
				$S.notice(message);
				setTimeout(function(){
					document.location = '/user/postinfor/new';
				}, 3000);
			} else {
				$S.alert(message);
				elements.delay(1000).removeAttr('disabled');
			}
		},
		error: function() {
			$S.error('发生技术问题，操作失败。请联系技术开发部');
			elements.delay(2000).removeAttr('disabled');
		}
	});
});

(function($,$S){
	if (typeof $S.Infor == 'undefined') {
		$S.Infor = {}; // 定义 StuCampus.Infor 命名空间
	}

	/**
	 * 定义后台删除信息函数
	 */
	$S.Infor.remove = function(id){
		$.ajax({
			url: '/infor/' + id,
			type: 'delete',
			statusCode: {
				403: function() {
					$S.alert('权限不足，删除失败');
				},
				404: function () {
					$S.alert('编号为 ' + id + ' 的信息不存在或已经删除');
				},
				500: function() {
					$S.error('发生技术问题，删除失败。请联系技术开发部');
				}
			},
			success: function() {
				$('form#infor').find('input, textarea').attr('disabled', 'disabled');
				$S.notice('删除成功');
				setTimeout(function(){
					document.location = '/user/postinfor/new';
				}, 3000);
			}
		});
	};

})(jQuery, StuCampus);
