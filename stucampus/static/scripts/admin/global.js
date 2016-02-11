(function($, $S){
	$S.initEditor = function(textarea, height, css){
		if (typeof height == 'undefined'){
			height = '400px';
		}
		if (typeof css == 'undefined'){
			css = '/static/styles/news/editor.css';
		}
		textarea.ckeditor({
			contentsCss: css,
			height: height,
		});
	}
})(jQuery, StuCampus);

// 为后台 tab 添加 class="current" 样式
$(function(){
	// 捕获当前 url 和 tab 的 url
	// 如果 tab-url 在 document-url 中出现（字符串匹配）
	// 则认为 tab-url 对应当前页面
	// 为 tab-url 对应的 li 节点添加 class="current" 样式
	var thisUrl = location.pathname.toLowerCase();
	var group   = $('#layout_left a[href="' + thisUrl + '"]').addClass('current');
});
