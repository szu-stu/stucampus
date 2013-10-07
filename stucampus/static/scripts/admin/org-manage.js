$(function(){
	org_edit = function(id){
        var phone = $("#phone").val();
        var homepage = $("#url").val();
        var logo = $("#logo").val();
        var url = '/manage/organization/' + id + '/edit';
        var method = 'post';
        var data = {'phone': phone, 'url': homepage, 'logo': logo, 'tips_type': 'message-box'};
        var status = {'success': '修改成功'}
        $S.ajax(url, method, {'data': data, 'status': status, 'tips_type': 'message-box'});
    };
});
