;(function($)
{
	// 窗口滑动加载 start
	var loadingStatus = false;
	$(window).scroll(function(){
            var scrollPos = $(document).scrollTop(); //滚动条距离顶部的高度
            var windowHeight = $(window).height(); //窗口的高度
            var dbHiht = $(document).height(); //整个页面文件的高度
            var page_number =$(".page_number").last().text()
            if(dbHiht - windowHeight <= scrollPos && page_number!="没有更多文章了"){
            	if(loadingStatus==true){
            			return false;
            	}
            	loadingStatus=true;
            	getNextTimes = parseInt(page_number) + 1;
            	setTimeout(function(){

            	$.ajax({
            			type: "GET",
            			url: "?page="+getNextTimes,
            			dataType: "html",
            			beforeSend: function(XMLHttpRequest){
            				$(".loader1").removeClass('hide').addClass('show');
            			},
            			success: function(data){
            				$(".plan_list ul").append(data);
            			},
            			error: function(data, status, e){
            				console.log(data);
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
        		$.ajax({
            				type: "POST",
            				url: "/summer_plans/add_plan/",
            				data:$("#plan_form").serialize(),
            				dataType: "json",
            				beforeSend: function(XMLHttpRequest){
            					$(".loader3").removeClass('hide').addClass('show');
            				},
            				success: function(data){
            					if(data.status=="success"){
            						alert("发表成功");
            						location.reload();
            					}
            					else{
            						$("#plan_form_error").text(data.messages);
            					}
            				},
            				error: function(data, status, e){
            					$("#plan_form_error").text(data);
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
        	var plan_id = $(this).data('plan_id');
        	console.log(plan_id);
        	$.ajax({
            				type: "GET",
            				url: "/summer_plans/like/"+"?plan_id="+plan_id,
            				dataType: "json",
            				beforeSend: function(XMLHttpRequest){
            					$(".loader3").removeClass('hide').addClass('show');
            				},
            				success: function(data){
            					if(data.status=="success"){
            						if (data.like_persons.length==0){
            							$('#like_persons_wrapper'+plan_id).addClass('hide');//人数为空就隐藏
            						}
            						else
            						{
            							$('#like_persons_wrapper'+plan_id).removeClass('hide');
            							var like_person_str="";
            							for (var i=0;i<data.like_persons.length;i++){
            								like_person_str+=data.like_persons[i].szu_name+",";
            							}
            							$("#like_persons"+plan_id).text(like_person_str);

            						}
            						
            					}
            					else{
            						alert(data.messages);
            					}
            					
            				},
            				error: function(data, status, e){
            					console.log(data);
            				},
            				complete:function(XMLHttpRequest){
            					loadingStatus = false;
            					$(".loader3").removeClass('show').addClass('hide');
            				}
            			});
        	
        });
        // 点赞功能 end
        

    })(jQuery);