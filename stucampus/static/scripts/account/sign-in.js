$(function(){
    var status = {'success': '登录成功',
                  'user_not_valid': '邮箱或密码错误',
                  'user_not_active': '该用户被停用，'}

    $S.ajaxForm($('#sign-in-form'), {'status': status});

    $('#sign-up-btn').click(function(){
        document.location = '/account/signup';
    });

    // 登录框就不要多此一举出现了
    $('#signer-box').remove();
});
