$(function(){
    var status = {'success': '登录成功'}

    $S.ajaxForm($('#sign-in-form'), {'status': status, 'tips_type': 'message-box'});

    $('#sign-up-btn').click(function(){
        document.location = '/account/signup';
    });

    $('#signer-box').remove();
});
