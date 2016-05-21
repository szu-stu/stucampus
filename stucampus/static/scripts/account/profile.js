// $(function () {
//     //生日日期插件
//     $(":date").dateinput({
//     format: 'yyyy-mm-dd',
//     selectors: true,
//     yearRange: [-40,10],
//     min: -20000,
//     max: 10000
//     });
// });

$(function() {
    //绑定表单ajax

    var status = {'success': '修改成功'};
    $S.ajaxForm($('#changeInfor'), {'status': status, 'tips_type': 'message-box'});
    $('#signer-box').remove();
});
