$(function(){
    var status = {'success': '登录成功'}

    $S.ajaxForm($('#sign-in-form'), {'status': status});

    $('#sign-up-btn').click(function(){
        document.location = '/account/signup';
    });

    // 登录框就不要多此一举出现了
    $('#signer-box').remove();
});
