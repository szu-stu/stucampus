$(function(){ 
	// 加载所见即所得编辑器
	$('#infor-content').ckeditor({
		contentsCss: '/static/styles/news/editor.css',
		height: '400px'
	});
	
	// 绑定表单 ajax
	var elements = $('#infor-form').find('input, textarea');
	$('#infor-form').ajaxForm({
		beforeSubmit: function(){
			elements.attr('disabled', 'disabled');
		},
		success: function(response){
			var messages = response.messages.join("、");
			if (response.success) {
				$S.notice(messages);
				setTimeout(function(){
					document.location = '/manage/infor/list';
				}, 3000);
			} else {
				$S.alert(messages);
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

	$S.Infor.edit = function(id){
        var title = $("#title").val();
        var organization_id = $("#organization_id").val();
        var content = $("#infor-content").val();
        $.ajax({
            url: '/manage/infor/' + id,
            type: 'put',
            dataType: 'json',
            data: {'title': title,
                   'organization_id': organization_id,
                   'content': content},
            success: function(response)
            {
                if (response.success)
                {
                    $S.notice('修改成功', 3000);
                    setTimeout(function(){
					   document.location.reload();
				    }, 3000);
                } else{
                    $S.alert(response.messages.join('、'), 3000);
                }
            }
        });
    };
	/**
	 * 定义后台删除信息函数
	 */
	$S.Infor.remove = function(id){
		$.ajax({
			url: '/manage/infor/' + id,
			type: 'delete',
			statusCode: {
				403: function() {
					$S.alert('权限不足，删除失败', 3000);
				},
				404: function () {
					$S.alert('编号为 ' + id + ' 的信息不存在或已经删除', 3000);
				},
				500: function() {
					$S.error('发生技术问题，删除失败。请联系技术开发部');
				} 
			},
			success: function() {
				$('form#infor').find('input, textarea').attr('disabled', 'disabled');
				$S.notice('信息删除成功', 3000);
				setTimeout(function(){
					document.location = '/manage/infor/list';
				}, 3000);
			}
		});
	};
	
})(jQuery, StuCampus);
