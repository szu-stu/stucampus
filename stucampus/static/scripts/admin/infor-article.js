$(function(){
    // 加载所见即所得编辑器
    $S.initEditor($('#infor-content'));

    // 绑定表单 ajax
    var status = {'success': '发布成功'};
    $S.ajaxForm($('#infor-form'), {'status': status, 'tips_type': 'message-box'});
});

(function($,$S){
    if (typeof $S.Infor == 'undefined') {
        $S.Infor = {};
    }

    $S.Infor.edit = function(id){
        var title = $("#title").val();
        var organization_id = $("#organization_id").val();
        var content = $("#infor-content").val();
        var url = '/manage/infor/' + id;
        var method = 'PUT';
        var data = {'title': title,
                    'organization_id': organization_id,
                    'content': content};
        var status = {'success': '修改成功', }
        $S.ajax(url, method, {'data': data, 'status': status, 'tips_type': 'message-box'});
    };

    $S.Infor.remove = function(id){
        var url = '/manage/infor/' + id;
        var method = 'DELETE';
        var status = {'success': '删除成功'};
        $S.ajax(url, method, {'status': status, 'tips_type': 'message-box'});
    };

})(jQuery, StuCampus);
