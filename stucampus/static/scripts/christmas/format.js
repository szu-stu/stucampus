/**
 * Created by wueiz on 2016/11/29.
 */
// 反正就是用来把页面的元素改成正确的东西就对了= =、
$(function () {
    //处理性别
    var $gender = $(".aim_group");
    var $value = $gender.find(".weui-form-preview__value");
    for(var i=0;i<$value.length;i++){
        if($value[i].innerHTML=="male")
            $value[i].innerHTML = "男";
        else if($value[i].innerHTML=="female")
            $value[i].innerHTML = "女";
        else if($value[i].innerHTML == "both")
            $value[i].innerHTML = "男女不限";
    }

    //处理匿名
    var $annoy = $(".annoymous");
    var $value = $annoy.find(".weui-form-preview__value");
    for(var i=0;i<$value.length;i++){
        if($value[i].innerHTML == "True")
            $value[i].innerHTML = "是";
        else
            $value[i].innerHTML = "否";
    }

    //处理宿舍区
    var $area = $(".own_area");
    var area_dict = {
        "A" : "西南",
        "B" : "斋区",
        "C" : "南区"
    };
    var $value = $area.find(".weui-form-preview__value");
    for(var i=0;i<$value.length;i++){
        $value[i].innerHTML = area_dict[$value[i].innerHTML];
    }

    //处理礼物类别
    var $type = $(".gift_type");
    var type_dict = {
        "01" : "食物",
        "02" : "服装配饰",
        "03" : "钟表首饰",
        "04" : "化妆品",
        "05" : "运动户外",
        "06" : "电器数码",
        "07" : "小玩意",
        "08" : "手工物件",
        "09" : "二次元",
        "10" : "图书音像",
        "11" : "学习资源",
        "12" : "其它"
    };
    var $value = $type.find(".weui-form-preview__value");
    for(var i=0;i<$value.length;i++){
        $value[i].innerHTML = type_dict[$value[i].innerHTML];
    }

    var $wanttype = $(".want_gift_type");
    var $value = $wanttype.find(".weui-form-preview__value");
    for(var i=0;i<$value.length;i++){
        var temp =  $value[i].innerHTML.split(" ");
        var res = "";
        for(var j=0;j<temp.length;j++){
            if(temp[j].length==2){
                res = res + type_dict[temp[j]] + " ";
            }
        }
        $value[i].innerHTML = res;
    }
    var $status = $(".gift_status");
    var $value = $status.find(".weui-form-preview__value");
    for(var i=0;i<$value.length;i++){
        if($value[i].innerHTML=="False"){
            $value[i].innerHTML= "未收到您的礼物或未完成登记";
        }
        else{
            $value[i].innerHTML = "我们收到了您的礼物";
        }
    }
});

