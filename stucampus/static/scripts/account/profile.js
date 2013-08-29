$(function () {
    //生日日期插件
    $(":date").dateinput({
    format: 'yyyy-mm-dd',
    selectors: true,
    yearRange: [-40,10],
    min: -20000,
    max: 10000
    });
});

$(function() {
    //绑定表单ajax
    var status = {'success': '修改成功',
                  'wrong_password': '密码错误',
                  'passwords_not_match': '密码不匹配'}
    $S.ajaxForm($('#changeInfor'), {'status': status});
});
