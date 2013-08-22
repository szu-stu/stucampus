$(function(){
	org_edit = function(id){
        var phone = $("#phone").val();
        var url = $("#url").val();
        var logo = $("#logo").val();
        $.ajax({
            url: '/manage/organization/' + id + '/edit',
            type: 'POST',
            dataType: 'json',
            data: {'phone': phone, 'url': url, 'logo': logo},
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
});