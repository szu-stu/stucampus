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
    $S.ajaxForm($('#changeInfor'));
});
