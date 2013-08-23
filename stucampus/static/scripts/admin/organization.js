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
            url: '/manage/organization/list',
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
        })
    }
})(jQuery, StuCampus);

