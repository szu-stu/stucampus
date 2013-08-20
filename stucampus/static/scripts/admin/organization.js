/* 组织 */

(function($,$S){
    if (typeof $S.Organization == 'undefined'){
        $S.Organization = {};//定义组织命名Stucampus.Organization空间
    }

    /**
    * 定义快速创建组织函数
    */
    $S.Organization.create = function(){
        var name = $("#name").val();
        var phone = $("#phone").val();
        $.ajax({
            url: '/manage/organization',
            type: 'POST',
            dataType: 'json',
            data: {'name': name, 'phone': phone},
            success: function(response)
            {
                if (response.success)
                {
                    $S.notice('添加成功', 3000);
                    setTimeout(function(){
					   document.location.reload();
				    }, 3000);
                } else{
                    $S.alert(response.messages.join('、'), 3000);
                }
            }
        });
    };

    $S.Organization.add_manager = function(id){
        var email = $("#org-"+id).val();
        $.ajax({
            url: '/manage/organization/' + id + '/manager',
            type: 'POST',
            data: {
                'email' : email,
            },
            success: function(response)
            {
                if (response.success)
                {
                    $S.notice('添加成功!', 3000);
                    setTimeout(function(){
                        document.location.reload()
                    }, 3000);
                } else {
                    $S.alert(response.messages.join(', '), 3000);
                }
            }
        }); 
    }

    $S.Organization.removeManager = function(id) {
        $.ajax({
            url: '/organization-manager/' + id,
            type: 'delete',
            success:function(response)
            {
                if (response.success)
                {
                    $S.notice(response.message, 3000);
                    setTimeout(function(){
                        document.location.reload();
                    }, 3000);
                } else {
                    $S.alert(response.message.join('、'), 3000);
                }
            }
        });
    }

    $S.Organization.edit = function(id) {
        var name = $('#name').val();
        var phoneNumber = $('#phoneNumber').val();
        var websiteAddress = $('#websiteAddress').val();
        var introduce = $('#introduce').val();
        $.ajax({
            url: '/admin/organization/' + id,
            type: 'PUT',
            data: {
                'name': name,
                'phoneNumber': phoneNumber,
                'websiteAddress': websiteAddress,
                'introduce': introduce
            },
            success: function(response)
            {
                if (response.success)
                {
                    $S.notice(response.message, 3000);
                    setTimeout(function() {
                    document.location.reload()
                    }, 3000);
                } else {
                    $S.alert(response.message);
                }
            }
        });
    }

    $S.Organization.remove = function(id) {
        $.ajax({
            url: '/manage/organization/' + id,
            type: 'delete',
            success: function(response){
                if (response.success) {
                    $S.notice('删除成功', 3000);
                    setTimeout(function(){document.location.reload()}, 3000);
                } else {
                    $S.alert(response.messages.join("、"), 3000);
                    setTimeout(function(){document.location.reload()});
                }
            }
        })}

/*组织发布信息*/
$(function(){
	// 加载所见即所得编辑器
	$('#content').ckeditor({
		contentsCss: '/static/styles/news/editor.css',
		height: '500px'
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
					document.location = '/activity/new';
				}, 3000);
			} else {
				$S.alert(message);
				elements.delay(1000).removeAttr('disabled');
			}
		},
		error: function() {
			$S.error('发生技术问题，操作失败。请联系学子天地技术开发部');
			elements.delay(2000).removeAttr('disabled');
		}
	});
});
})(jQuery, StuCampus);

