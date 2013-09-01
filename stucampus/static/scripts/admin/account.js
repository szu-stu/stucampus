(function($,$S){
    if (typeof $S.Account == 'undefined'){
        $S.Account = {};
    };

    $S.Account.ban = function(id){
        url = '/manage/account/' + id;
        method = 'PUT';
        var data = {'is_ban': True};
        var status = {'success': '操作成功',
                      'user_is_admin': '不能禁用管理员'};
        $S.ajax(url, method, {'data': data, 'status': status})
    };

    $S.Account.remove = function(id) {
        url = '/manage/account/' + id;
        method = 'DELETE';
        var status = {'success': '删除成功',
                      'user_is_admin': '不能删除管理员!'};
        $S.ajax(url, method, {'status': status});
    };
})(jQuery, StuCampus);
