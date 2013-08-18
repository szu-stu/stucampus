$(document).ready(function(){
	//首页幻灯片 
	$("#news-slider").bjqs({
		'width'		: 605,
		'height'	: 415,
	    'animationDuration' : 800,
	    'centerMarkers' : true,
	    'centerControls' :false,
	    'nextText': '<i class="icon-chevron-right icon-white"></i>',
	    'prevText': '<i class="icon-chevron-left icon-white"></i>',
	    'useCaptions' : true,
	    'keyboardNav' : true
	});	
});

$(function(){
	$("#inforbox").scrollable({
		vertical: true,
		mousewheel: true,
		items: 'ul#infors'
	});
	
	var inforScroll = $('#inforbox').data('scrollable');
	
	$('#infor-up').click(function(){ 
		inforScroll.prev(100).prev(100).prev(100);
	});
	
	$('#infor-down').click(function(){ 
		inforScroll.next(100).next(100).next(100); 
	});		
});