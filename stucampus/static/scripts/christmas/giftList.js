$(function (){
    $('#gift-btn').on('click', function (){
        $.weui.actionSheet([{
            label: '交换礼物',
            onClick: function (){
                window.location.href="/christmas/exchange/";
            }
        },{
            label: '送给指定人',
            onClick: function (){
                window.location.href="/christmas/given/";
            }
        }]);
    });
    $(".choice-type-btn").on('click', function () {
        var $me = this;
        var $dialog = $("#checkbox_dialog");
        $dialog.fadeIn(200);
        $(document.body).css("overflow","hidden");
        $("#yes").on('click', function () {
            console.log($me);
            var a = $('input:checked');
            var result_array = [];
            var val = $me.attributes['data'].value;
            for(var i=0;i<a.length;i++){
                result_array.push(a[i].name);
            }
            $(document.body).css("overflow","auto");
            //传进某个url进行处理
            $.ajax({
                url: "/christmas/postWantType/",
                type: "POST",
                data: {
                    'wanttype[]': result_array,
                    'giftId': val
                },
                success: function (response) {
                    if (response.status == "success") {
                        $me.remove();
                        $.weui.toast(response.message);
                        setTimeout(function() {
                            window.location.href = "/christmas/giftList/";
                        }, 1500);
                        // 改变按钮类型，反正就是删除就对了
                    }
                    else if(response.status == "resubmit"){
                        console.log(response.message);
                        $me.remove();
                        $.weui.topTips(response.message);
                        setTimeout(function() {
                            window.location.href = "/christmas/giftList/";
                        }, 1500);
                        // 都是错误就一并删除了吧
                    }
                    else if(response.status == "error"){
                        //不要乱来啊亲= =、
                    }
                }
            });
            //删除操作，指的是删除那个啥，全部选定项目
            $dialog.fadeOut(200);
        });
        $("#no").on('click', function () {
            $dialog.fadeOut(200);
            $(document.body).css("overflow","auto");
        })
    });
            //下面那坨东西我原本是以为要直接选的，然后发现不是那个做法，于是估摸着报废了，不过可以看看当作例子啥的= =、，对应把views里的postWantType取消注释了就行， 噢，还有giftList.html的注释= =、
            // $(".choice-type-btn").on('click', function () {
            //     var me = this;
            //     weui.picker([{
            //         label: '食物',
            //         value: '01'
            //     }, {
            //         label: '服装配饰',
            //         value: '02'
            //     }, {
            //         label: '钟表首饰',
            //         value: '03'
            //     },{
            //         label: '化妆品',
            //         value: '04'
            //     }, {
            //         label: '运动户外',
            //         value: '05'
            //     }, {
            //         label: '电器数码',
            //         value: '06'
            //     }, {
            //         label: '小玩意',
            //         value: '07'
            //     }, {
            //         label: '手工物件',
            //         value: '08'
            //     }, {
            //         label: '二次元',
            //         value: '09'
            //     }, {
            //         label: '图书音像',
            //         value: '10'
            //     }, {
            //         label: '学习资源',
            //         value: '11'
            //     }, {
            //         label: '其它',
            //         value: '12'
            //     }], {
            //         onConfirm: function (result) {
            //             var $iosDialog = $('#iosDialog');
            //             $iosDialog.fadeIn(200);
            //             $('#confirm-content').html("您确定设置" + result + "为您想要的礼物类别吗？");
            //             $('#yes').on('click', function () {
            //                 console.log("确认");
            //                 var val = me.attributes['data'].value;
            //                 $.ajax({
            //                     url: "/postWantType/",
            //                     type: "POST",
            //                     data: {
            //                         wanttype: result,
            //                         giftId: val
            //                     },
            //                     success: function (response) {
            //                         if (response.status == "success") {
            //                             result = "";
            //                             val = "";
            //                             me.remove();
            //                             // 改变按钮类型，反正就是删除就对了
            //                         }
            //                         else if(response.status == "error"){
            //                             result = "";
            //                             val = "";
            //                             me.remove();
            //                             // 都是错误就一并删除了吧
            //
            //                         }
            //                         else if(response.status == "nogift"){
            //                             // 这种类型礼物没了，不需要清空，但需要提示选其他礼物类别
            //                         }
            //                         else if(response.status == "resubmit"){
            //                             // 对于这种情况，我也是很无奈。。燃鹅就是不知道咋改好= =、不如不改了
            //                         }
            //                     }
            //                 });
            //                 $iosDialog.fadeOut(200);
            //             })
            //             $('#no').on('click', function () {
            //                 console.log("不确认");
            //                 $iosDialog.fadeOut(200);
            //             });
            //         }
            //     });
            // });
});
$(function () {
    $a = $("h4");
    if($a.length===1){
        $.weui.topTips("您还没有礼物");
    }
});
