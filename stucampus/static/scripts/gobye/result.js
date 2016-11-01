// 重置所有操作
$(function () {
    $all = $("body").html();
});
var $all;
function reset() {
    $("body").html($all);
}
// 移动一门课程
function move_one(e) {
    selectedValue = $(e).val();
    selectedText = $(e).find("option:selected").text();
    if (selectedValue === "null") {
        return 
    }
    htmlCode = '<select onchange="move_one(this)"><option value="null">无</option><option value="failed">标记挂科</option><option value="public-must">标记公共必修</option><option value="profession-must">标记专业必修</option><option value="profession-select">标记专业选修</option><option value="arts-public-select">标记公共选修(文科)</option><option value="science-public-select">标记公共选修(理科)</option><option value="double">标记双修</option></select>';
    var $tr = $(e).parent().parent();
    htmlCode = htmlCode.replace('<option value="' + selectedValue + '">' + selectedText + '</option>', "");
    if (selectedValue.indexOf("arts") != -1) {
        $tr.find("td").eq(6).text("文");
        selectedValue = selectedValue.substr(5);
    } else if (selectedValue.indexOf("science") != -1) {
        $tr.find("td").eq(6).text("理");
        selectedValue = selectedValue.substr(8);
    }
    $tr.find("td:last").html(htmlCode);
    $("<tr>" + $tr.html() + "</tr>").insertBefore("." + selectedValue + " tbody tr:last");
    $tr.remove();
    calculate();
}
// 批量移动
function move_all(e) {
    selectedValue = $(e).val();
    if (selectedValue == "null") {
        return 
    }
    $tbody = $(e).parent().parent().parent();
    $checkbox = $tbody.find('input:checked');
    $select = $checkbox.eq(0).parent().parent().find("select:first");
    $select.val(selectedValue);
    $select.trigger("change");
    if ($checkbox.length > 1) {
        move_all(e);
    } else {
        $(e).val("null");
    }
}