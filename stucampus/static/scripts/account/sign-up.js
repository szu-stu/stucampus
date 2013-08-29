$(function(){
    var status = {'success': '注册成功',
                  'passwords_not_match': '确认密码不匹配',
                  'email_existed': '邮箱已存在'}
    $S.ajaxForm($('#sign-up-form'), {'status': status});
});
