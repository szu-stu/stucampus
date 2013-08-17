function Base64() {  
    // private property  
    _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";  
    // public method for encoding  
    this.encode = function (input) {  
        var output = "";  
        var chr1, chr2, chr3, enc1, enc2, enc3, enc4;  
        var i = 0;  
        input = _utf8_encode(input);  
        while (i < input.length) {  
            chr1 = input.charCodeAt(i++);  
            chr2 = input.charCodeAt(i++);  
            chr3 = input.charCodeAt(i++);  
            enc1 = chr1 >> 2;  
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);  
            enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);  
            enc4 = chr3 & 63;  
            if (isNaN(chr2)) {  
                enc3 = enc4 = 64;  
            } else if (isNaN(chr3)) {  
                enc4 = 64;  
            }  
            output = output +  
            _keyStr.charAt(enc1) + _keyStr.charAt(enc2) +  
            _keyStr.charAt(enc3) + _keyStr.charAt(enc4);  
        }  
        return output;  
    }  
    // public method for decoding  
    this.decode = function (input) {  
        var output = "";  
        var chr1, chr2, chr3;  
        var enc1, enc2, enc3, enc4;  
        var i = 0;  
        input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");  
        while (i < input.length) {  
            enc1 = _keyStr.indexOf(input.charAt(i++));  
            enc2 = _keyStr.indexOf(input.charAt(i++));  
            enc3 = _keyStr.indexOf(input.charAt(i++));  
            enc4 = _keyStr.indexOf(input.charAt(i++));  
            chr1 = (enc1 << 2) | (enc2 >> 4);  
            chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);  
            chr3 = ((enc3 & 3) << 6) | enc4;  
            output = output + String.fromCharCode(chr1);  
            if (enc3 != 64) {  
                output = output + String.fromCharCode(chr2);  
            }  
            if (enc4 != 64) {  
                output = output + String.fromCharCode(chr3);  
            }  
        }  
        output = _utf8_decode(output);  
        return output;  
    }  
    // private method for UTF-8 encoding  
    _utf8_encode = function (string) {  
        string = string.replace(/\r\n/g,"\n");  
        var utftext = "";  
        for (var n = 0; n < string.length; n++) {  
            var c = string.charCodeAt(n);  
            if (c < 128) {  
                utftext += String.fromCharCode(c);  
            } else if((c > 127) && (c < 2048)) {  
                utftext += String.fromCharCode((c >> 6) | 192);  
                utftext += String.fromCharCode((c & 63) | 128);  
            } else {  
                utftext += String.fromCharCode((c >> 12) | 224);  
                utftext += String.fromCharCode(((c >> 6) & 63) | 128);  
                utftext += String.fromCharCode((c & 63) | 128);  
            }  
   
        }  
        return utftext;  
    }  
    // private method for UTF-8 decoding  
    _utf8_decode = function (utftext) {  
        var string = "";  
        var i = 0;  
        var c = c1 = c2 = 0;  
        while ( i < utftext.length ) {  
            c = utftext.charCodeAt(i);  
            if (c < 128) {  
                string += String.fromCharCode(c);  
                i++;  
            } else if((c > 191) && (c < 224)) {  
                c2 = utftext.charCodeAt(i+1);  
                string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));  
                i += 2;  
            } else {  
                c2 = utftext.charCodeAt(i+1);  
                c3 = utftext.charCodeAt(i+2);  
                string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));  
                i += 3;  
            }  
        }  
        return string;
    }  
}  


String.format = function(src){
    if (arguments.length == 0) return null;
    var args = Array.prototype.slice.call(arguments, 1);
    return src.replace(/\{(\d+)\}/g, function(m, i){
        return args[i];
    });
};

/**
 * 上传首页图片
 * @param targetID	目标文本框的ID
 */
function uploadFile(targetID){
	var base64 = new Base64();
	var js = 'function(resultName) {$(window.opener.document.getElementById("' + targetID + '")).attr("value", "/upfiles/" + resultName);}';
	window.open('/admin/upload/' + base64.encode(js), '后台上传工具', 'width=350,height=165,status=y0,scorllbars=0,resizable=0,menuable=0,location=0,directories=0');		
}

/**
 * 上传图片到编辑器
 * @param editorID 编辑器ID
 */
function uploadImageToCKeditor(editorID){
	var base64 = new Base64();
	var js = 'function(resultName) {$(window.opener.CKEDITOR.instances.' + editorID + '.insertHtml(\'<img src="/upfiles/\' + resultName + \'" alt="" onload="javascript:if(this.width>660)this.width=595" />\'));}';
	window.open('/admin/upload/' + base64.encode(js), '后台上传工具', 'width=350,height=165,status=y0,scorllbars=0,resizable=0,menuable=0,location=0,directories=0');
}

/**
 * 上传文件到编辑器（提供下载）
 * @param editorID 编辑器ID
 */
function uploadFileToCKeditor(editorID){
	var base64 = new Base64();
	var js = 'function(resultName) {$(window.opener.CKEDITOR.instances.' + editorID + '.insertHtml(\'<a href="/upfiles/\' + resultName + \'" target="_blank" />\' + resultName + \'</a>\'));}';
	window.open('/admin/upload/' + base64.encode(js), '后台上传工具', 'width=350,height=165,status=y0,scorllbars=0,resizable=0,menuable=0,location=0,directories=0');	
}

 /**
 * 上传封面到杂志
 * @param targetID  目标文本框的ID
 */
function uploadCover(targetID){
    var base64 = new Base64();
    var js = 'function(resultName) {$(window.opener.document.getElementById("' + targetID + '")).attr("value", "/upfiles/yunyi/" + resultName);}';
    window.open('/magazine/upload/' + base64.encode(js), '杂志封面上传工具', 'width=350,height=165,status=y0,scorllbars=0,resizable=0,menuable=0,location=0,directories=0');     
}