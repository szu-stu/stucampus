$(function(){
    // 加载所见即所得编辑器
    $S.initEditor($('#infor-content'));

    // 绑定表单 ajax
    $S.ajaxForm($('#infor-form'));
});

(function($,$S){
    if (typeof $S.Infor == 'undefined') {
        $S.Infor = {};
    }

    $S.Infor.edit = function(id){
        var title = $("#title").val();
        var organization_id = $("#organization_id").val();
        var content = $("#infor-content").val();
        url = '/manage/infor/' + id;
        method = 'PUT';
        data = {'title': title,
                'organization_id': organization_id,
                'content': content};
        $S.ajax(url, method, data);
    };

    $S.Infor.remove = function(id){
        url = '/manage/infor/' + id;
        method = 'DELETE';
        $S.ajax(url, method);
    };

})(jQuery, StuCampus);
