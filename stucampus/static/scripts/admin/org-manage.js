$(function(){
	org_edit = function(id){
        var phone = $("#phone").val();
        var homepage = $("#url").val();
        var logo = $("#logo").val();
        url = '/manage/organization/' + id + '/edit';
        method = 'POST';
        $S.ajax(url, method, data);
        data = {'phone': phone, 'url': homepage, 'logo': logo};
    };
});
