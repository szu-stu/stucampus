(function($,$S){
    if (typeof $S.Account == 'undefined'){
        $S.Account = {};
    };

    $S.Account.ban = function(id){
        url = '/manage/account/' + id;
        method = 'PUT';
        data = {'is_ban': True};
        $S.ajax(url, method, data)
    };

    $S.Account.remove = function(id) {
        url = '/manage/account/' + id;
        method = 'DELETE';
        $S.ajax(url, method);
    };
})(jQuery, StuCampus);
