/* 用户 */

(function($,$S){
    if (typeof $S.Account == 'undefined'){
        $S.Account = {};  //定义组织命名 Stucampus.Account 空间
    }

    $S.Account.ban = function(id) {
        $.ajax({
            url: '/manage/account/' + id,
            type: 'PUT',
            success: function(response)
            {
                if (response.success)
                {
                    $S.notice(response.messages, 3000);
                    setTimeout(function() {
                        document.location.reload()
                    }, 3000);
                } else {
                    $S.alert(response.messages.join(','), 3000);
                }
            }
        });
    }

    $S.Account.remove = function(id) {
        $.ajax({
            url: '/manage/account/' + id,
            type: 'delete',
            success: function(response){
                if (response.success) {
                    $S.notice('删除成功', 3000);
                    setTimeout(function(){
                        document.location.reload()
                    }, 3000);
                } else {
                    $S.alert(response.messages.join(","), 3000);
                }
            }
        })
    }
})(jQuery, StuCampus);

