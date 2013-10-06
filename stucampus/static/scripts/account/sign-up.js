$(function(){
    var status = {'success': '注册成功'}
    $S.ajaxForm($('#sign-up-form'), {'status': status, 'tips_type': 'message-box'});
});
