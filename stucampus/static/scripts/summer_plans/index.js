;(function($)
{
	function UrlUpdateParams(name, value) {
		var r = window.location.href;
		var url = window.location.href;
		if (r != null && r != 'undefined' && r != "") {
			value = encodeURIComponent(value);
			var reg = new RegExp("(^|)" + name + "=([^&]*)(|$)");
			var tmp = name + "=" + value;
			if (url.match(reg) != null) {
				r = url.replace(eval(reg), tmp);
			}
			else {
				if (url.match("[\?]")) {
					r = url + "&" + tmp;
				} else {
					r = url + "?" + tmp;
				}
			}
		}
		return r;
	}

	// 窗口滑动加载 start
	var loadingStatus = false;
	$(window).scroll(function(){
            var scrollPos = $(document).scrollTop(); //滚动条距离顶部的高度
            var windowHeight = $(window).height(); //窗口的高度
            var dbHiht = $(document).height(); //整个页面文件的高度
            var page_number =$(".page_number").last().text()
            if(dbHiht - windowHeight <= scrollPos && page_number!="没有更多了"){
            	if(loadingStatus==true){
            			return false;
            	}
            	loadingStatus=true;
            	getNextTimes = parseInt(page_number) + 1;
            	setTimeout(function(){

            	$.ajax({
            			type: "GET",
            			url: UrlUpdateParams("page",getNextTimes),
            			dataType: "html",
            			beforeSend: function(XMLHttpRequest){
            				$(".loader1").removeClass('hide').addClass('show');
            			},
            			success: function(data){
            				$(".plan_list ul").append(data);
            			},
            			error: function(data, status, e){
            				alert("出现错误，请联系qq：649743466");
            			},
            			complete:function(XMLHttpRequest){
            				loadingStatus = false;
            			$(".loader1").removeClass('show').addClass('hide');
            			}
            		});
            	},100);
            }
            
        });
        // 窗口滑动加载 end
        // 发表计划 start
        $("#submit_plan_form").click(
        	function(){
        		var url=$("#submit_plan_form").data("url");
        		$.ajax({
            				type: "POST",
            				url: url,
            				data:$("#plan_form").serialize(),
            				dataType: "json",
            				success: function(data){
            					if(data.status=="success"){
            						alert("发表成功");
                                    $('#form_modal').modal('hide');
            						location.reload();
            					}
            					else{
            						$("#plan_form_error").text(data.messages);
            					}
            				},
            				error: function(data, status, e){
            					$("#plan_form_error").text("出现错误，请联系qq：649743466");
            				},
            				complete:function(XMLHttpRequest){
            					loadingStatus = false;
            					$(".loader3").removeClass('show').addClass('hide');
            				}
            			});
        	});
        // 发表计划 end

// 点赞功能 start
        $(".plan_list").delegate('.like_btn','click',function(){
        	var url = $(this).data('url');
        	var plan_id = $(this).data('plan_id')
        	$.ajax({
            				type: "GET",
            				url: url,
            				dataType: "json",
            				success: function(data){
            					if(data.status=="success"){
            						// 处理人名
            						if (data.like_persons.length==0){
            							$('#like_persons_wrapper'+plan_id).addClass('visi_hide');//人数为空就隐藏
            						}
            						else
            						{
            							$('#like_persons_wrapper'+plan_id).removeClass('visi_hide');
            							var like_person_str="";
            							var i=0;
            							for (i=0;i<data.like_persons.length-1;i++){
            								like_person_str+=data.like_persons[i].szu_name+",";
            							}
            							like_person_str+=data.like_persons[i].szu_name;
            							$("#like_persons"+plan_id).text(like_person_str);

            						}
            						//处理szu_no，判断是否点赞
            						var szu_no_str="";
            						for (var i=0;i<data.like_persons.length;i++){
            								szu_no_str+=data.like_persons[i].szu_no+",";
            								console.log(data.like_persons[i].szu_no);

            							}
            						var user_id = $("#user_id").text()
            						if (szu_no_str.indexOf(user_id)>=0)
            						{
            							$("#liked_tip"+plan_id).removeClass("visi_hide");
            						}
            						else
            						{	
            							$("#liked_tip"+plan_id).addClass("visi_hide");
            						}
            						
            					}
            					else{
            						alert(data.messages);
            					}
            					
            				},
            				error: function(data, status, e){
            					alert("您需要登录才能点赞，如果登录完还不能点赞，请联系qq：649743466")
            				},
            				complete:function(XMLHttpRequest){
            					loadingStatus = false;
            					$(".loader3").removeClass('show').addClass('visi_hide');
            				}
            			});
        	
        });
        // 点赞功能 end

        // 发表感想 start
        $(".plan_list").delegate('.post_thought','click',function(){
        	var url = $(this).data('url');
        	$("#submit_thought_form").data("url",url);
        	$('#thought_modal').modal('show');
        });

        $("#submit_thought_form").click(function(){
        	var url = $(this).data('url');
        	console.log(url);
        	$.ajax({
            				type: "POST",
            				url: url,
            				dataType: "json",
            				data:$("#thought_form").serialize(),
            				success: function(data){
            					if(data.status=="success"){
            						alert("发表成功");
                                    $('#thought_modal').modal('hide');
            						location.reload();
            					}
            					else{
            						$("#thought_form_error").text(data.messages);
            					}
            					
            				},
            				error: function(data, status, e){
            					$("#thought_form_error").text("出现错误，请联系qq：649743466");
            					console.log(data);
            				},
            			});
        });

        // 发表感想 end
        

    })(jQuery);