$(function(){
    $S.ajaxForm($('#sign_in-form'));

    $('#sign_up-btn').click(function(){
        document.location = '/account/signup';
    });

    // 登录框就不要多此一举出现了
    $('#signer-box').remove();
});
