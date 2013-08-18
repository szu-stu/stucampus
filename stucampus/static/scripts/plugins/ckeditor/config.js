/*
Copyright (c) 2003-2011, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.stylesSet.add( 'stucampus_styles',
[
    { name : '红色文字' , element : 'span', styles : { 'color' : 'red' } },
    { name : '蓝色文字' , element : 'span', styles : { 'color' : 'blue' } },
    { name : '绿色文字' , element : 'span', styles : { 'color' : 'green' } }
]);

CKEDITOR.editorConfig = function( config )
{
	// Define changes to default configuration here. For example:
	config.language = 'zh-CN';
	// config.uiColor = '#AADC6E';
	config.toolbar = 'Full';
	config.stylesSet = 'stucampus_styles';
	 
	config.toolbar_Full =
	[
		{ name:'document', items:['Source','-','Maximize', 'ShowBlocks', '-', 'DocProps','Preview','Print','-','Templates']},
		{ name:'clipboard', items : ['Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ] },
		{ name:'editing', items : ['Find','Replace','-','SelectAll','-','SpellChecker', 'Scayt' ] },
		{ name:'basicstyles', items : [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat' ] },
		{ name:'paragraph', items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv','-',
		                              'JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ] },
		{ name: 'links', items : [ 'Link','Unlink','Anchor' ] },
		{ name: 'insert', items : [ 'Image','Flash','Table','SpecialChar','PageBreak' ] },
		{ name: 'styles', items : [ 'Styles','Format','Font','FontSize' ] },
		{ name: 'colors', items : [ 'TextColor','BGColor' ] }
	];
	 
	config.toolbar_Basic =
	[
		['Bold', 'Italic', '-', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink']
	];
	
	config.format_tags = 'p;h3;h4;h5';
	config.resize_enabled = false;
};
