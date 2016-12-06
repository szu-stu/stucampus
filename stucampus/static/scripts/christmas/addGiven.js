$(function(){
            var options = {
                success: show,
                clearForm: false,
                timeout: 3000
            }
            function show(response) {
                var message = response.message;
                if(response.status=="success"){
                    $.weui.toast('提交成功<br/>'+response.message);
                    setTimeout(function() {
                        window.location.href = "/christmas/giftList/";
                    }, 1500);
                }
                else if(response.status=="error"){
                    var i=0;
                    var str_message = "";
                    for(i=0;i<message.length;i++){
                        str_message += message[i][0] + "<br/>";
                    }
                    $.weui.topTips(str_message);
                }
                else if(response.status=="full"){
                    $.weui.topTips(response.message);
                }
            }
            $("#my_form").ajaxForm(options);
            $("#my_form").submit(function () {
                return false;
            })
});
