$(document).ready(function(){
	$(".btn-get").click(function(){
		ele = this;
		$.ajax({
			type:"POST",
			url:"/christmas/manage/get",
			data:{uid:this.name},
			success:function(){
                               this.disabled = true;
			}
		})
	});
});
