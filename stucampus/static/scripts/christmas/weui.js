/*!
 * WeUI.js v0.3.0 (https://github.com/progrape/weui.js)
 * Copyright 2016
 * Licensed under the MIT license
 */
'use strict';

(function ($) {
    $.weui = {
        version: '0.3.0'
    };

    $.noop = $.noop || function () {};
})($);
'use strict';

(function ($) {

    var $dialog = null;

    /**
     *  weui dialog
     * @param {Object} [options]
     */
    $.weui.dialog = function (options) {
        options = $.extend({
            title: '标题',
            content: '内容',
            className: '',
            buttons: [{
                label: '确定',
                type: 'primary',
                onClick: $.noop
            }]
        }, options);

        var buttons = options.buttons.map(function (button) {
            return '<a href="javascript:;" class="weui_btn_dialog ' + button.type + '">' + button.label + '</a>';
        }).join('\n');
        var html = '<div class="' + options.className + '">\n                <div class="weui_mask"></div>\n                <div class="weui_dialog">\n                    <div class="weui_dialog_hd">\n                        <strong class="weui_dialog_title">\n                            ' + options.title + '\n                        </strong>\n                    </div>\n                    <div class="weui_dialog_bd">\n                        ' + options.content + '\n                    </div>\n                    <div class="weui_dialog_ft">\n                        ' + buttons + '\n                    </div>\n                </div>\n            </div>';
        $dialog = $(html);
        $('body').append($dialog);
        $dialog.on('click', '.weui_btn_dialog', function () {
            var button = options.buttons[$(this).index()];
            var cb = button.onClick || $.noop;
            cb.call();
            $.weui.closeDialog();
        });
    };

    /**
     * close dialog
     */
    $.weui.closeDialog = function () {
        if ($dialog) {
            $dialog.off('click');
            // zepto 核心不包含动画相关的方法
            if (typeof $dialog.fadeOut === 'function') {
                $dialog.fadeOut('fast', function () {
                    $dialog.remove();
                    $dialog = null;
                });
            } else {
                $dialog.remove();
                $dialog = null;
            }
        }
    };
})($);
'use strict';

(function ($) {
    /**
     * alert
     * @param {String} content
     * @param {Object} options
     * @param {Function} yes
     */
    $.weui.alert = function (content, options, yes) {

        var type = typeof options === 'function';
        if (type) {
            yes = options;
        }

        options = $.extend({
            title: '警告',
            content: content || '警告内容',
            className: '',
            buttons: [{
                label: '确定',
                type: 'primary',
                onClick: yes
            }]
        }, type ? {} : options);
        options.className = 'weui_dialog_alert ' + options.className;

        $.weui.dialog(options);
    };
})($);
'use strict';

(function ($) {

    var $topTips = null;
    var timer = null;

    /**
     * show top tips
     * @param {String} content
     * @param {Object|Number|Function} [options]
     */
    $.weui.topTips = function () {
        var content = arguments.length <= 0 || arguments[0] === undefined ? 'topTips' : arguments[0];
        var options = arguments[1];


        if ($topTips) {
            $topTips.remove();
            timer && clearTimeout(timer);
            $topTips = null;
        }

        if (typeof options === 'number') {
            options = {
                duration: options
            };
        }

        if (typeof options === 'function') {
            options = {
                callback: options
            };
        }

        options = $.extend({
            duration: 3000,
            callback: $.noop
        }, options);
        var html = '<div class="weui_toptips weui_warn">' + content + '</div>';
        $topTips = $(html);
        $topTips.appendTo($('body'));
        if (typeof $topTips.slideDown === 'function') {
            $topTips.slideDown(20);
        } else {
            $topTips.show();
        }

        timer = setTimeout(function () {
            if ($topTips) {
                if (typeof $topTips.slideUp === 'function') {
                    $topTips.slideUp(120, function () {
                        $topTips.remove();
                        $topTips = null;
                        options.callback();
                    });
                } else {
                    $topTips.remove();
                    $topTips = null;
                    options.callback();
                }
            }
        }, options.duration);
    };

    /**
     * hide topTips
     */
    $.weui.hideTopTips = function () {
        $topTips && $topTips.remove();
        $topTips = null;
    };
})($);
'use strict';

(function ($) {

    var $actionSheetWrapper = null;

    /**
     * show actionSheet
     * @param {Array} menus
     * @param {Array} actions
     */
    $.weui.actionSheet = function () {
        var menus = arguments.length <= 0 || arguments[0] === undefined ? [] : arguments[0];
        var actions = arguments.length <= 1 || arguments[1] === undefined ? [{ label: '取消' }] : arguments[1];

        var cells = menus.map(function (item, idx) {
            return '<div class="weui_actionsheet_cell">' + item.label + '</div>';
        }).join('');
        var action = actions.map(function (item, idx) {
            return '<div class="weui_actionsheet_cell">' + item.label + '</div>';
        }).join('');
        var html = '<div>\n            <div class="weui_mask_transition"></div>\n            <div class="weui_actionsheet">\n                <div class="weui_actionsheet_menu">\n                    ' + cells + '\n                </div>\n                <div class="weui_actionsheet_action">\n                    ' + action + '\n                </div>\n            </div>\n        </div>';

        $actionSheetWrapper = $(html);
        $('body').append($actionSheetWrapper);

        // add class
        $actionSheetWrapper.find('.weui_mask_transition').show().addClass('weui_fade_toggle');
        $actionSheetWrapper.find('.weui_actionsheet').addClass('weui_actionsheet_toggle');

        // bind event
        $actionSheetWrapper.on('click', '.weui_actionsheet_menu .weui_actionsheet_cell', function () {
            var item = menus[$(this).index()];
            var cb = item.onClick || $.noop;
            cb.call();
            $.weui.hideActionSheet();
        }).on('click', '.weui_mask_transition', function () {
            $.weui.hideActionSheet();
        }).on('click', '.weui_actionsheet_action .weui_actionsheet_cell', function () {
            var item = actions[$(this).index()];
            var cb = item.onClick || $.noop;
            cb.call();
            $.weui.hideActionSheet();
        });
    };

    $.weui.hideActionSheet = function () {
        if (!$actionSheetWrapper) {
            return;
        }

        var $mask = $actionSheetWrapper.find('.weui_mask_transition');
        var $actionsheet = $actionSheetWrapper.find('.weui_actionsheet');

        $mask.removeClass('weui_fade_toggle');
        $actionsheet.removeClass('weui_actionsheet_toggle');

        $actionsheet.on('transitionend', function () {
            $actionSheetWrapper.remove();
            $actionSheetWrapper = null;
        }).on('webkitTransitionEnd', function () {
            $actionSheetWrapper.remove();
            $actionSheetWrapper = null;
        });
    };
})($);
'use strict';

(function ($) {
    /**
     * confirm
     * @param {String} content
     * @param {String} options
     * @param {Function} yes
     * @param {Function} no
     */
    $.weui.confirm = function (content, options, yes, no) {

        var type = typeof options === 'function';
        if (type) {
            no = yes;
            yes = options;
        }

        options = $.extend({
            title: '确认',
            content: content || '确认内容',
            className: '',
            buttons: [{
                label: '取消',
                type: 'default',
                onClick: no || $.noop
            }, {
                label: '确定',
                type: 'primary',
                onClick: yes || $.noop
            }]
        }, type ? {} : options);
        options.className = 'weui_dialog_confirm ' + options.className;

        $.weui.dialog(options);
    };
})($);
"use strict";

/**
 * Created by bearyan on 2016/2/16.
 */
(function () {
    function _validate($input) {
        var input = $input[0],
            val = $input.val();

        if (input.tagName == "INPUT" || input.tagName == "TEXTAREA") {
            var reg = input.getAttribute("required") || input.getAttribute("pattern") || "";

            if (!$input.val().length) {
                return "empty";
            } else if (reg) {
                return new RegExp(reg).test(val) ? null : "notMatch";
            } else {
                return null;
            }
        } else if (input.getAttribute("type") == "checkbox" || input.getAttribute("type") == "radio") {
            // 没有正则表达式：checkbox/radio要checked
            return input.checked ? null : "empty";
        } else if (val.length) {
            // 有输入值
            return null;
        }

        return "empty";
    }
    function _showErrorMsg(error) {
        if (error) {
            var $dom = error.$dom,
                msg = error.msg,
                tips = $dom.attr(msg + "Tips") || $dom.attr("tips") || $dom.attr("placeholder");
            if (tips) $.weui.topTips(tips);
            $dom.parents(".weui_cell").addClass("weui_cell_warn");
        }
    }

    var oldFnForm = $.fn.form;
    $.fn.form = function () {
        return this.each(function (index, ele) {
            var $form = $(ele);
            $form.find("[required]").on("blur", function () {
                var $this = $(this),
                    errorMsg;
                if ($this.val().length < 1) return; // 当空的时候不校验，以防不断弹出toptips

                errorMsg = _validate($this);
                if (errorMsg) {
                    _showErrorMsg({
                        $dom: $this,
                        msg: errorMsg
                    });
                }
            }).on("focus", function () {
                var $this = $(this);
                $this.parents(".weui_cell").removeClass("weui_cell_warn");
            });
        });
    };
    $.fn.form.noConflict = function () {
        return oldFnForm;
    };

    var oldFnValidate = $.fn.validate;
    $.fn.validate = function (callback) {
        return this.each(function () {
            var $requireds = $(this).find("[required]");
            if (typeof callback != "function") callback = _showErrorMsg;

            for (var i = 0, len = $requireds.length; i < len; ++i) {
                var $dom = $requireds.eq(i),
                    errorMsg = _validate($dom),
                    error = { $dom: $dom, msg: errorMsg };
                if (errorMsg) {
                    if (!callback(error)) _showErrorMsg(error);
                    return;
                }
            }
            callback(null);
        });
    };
    $.fn.validate.noConflict = function () {
        return oldFnValidate;
    };
})();
'use strict';

(function ($) {
    var $loading = null;

    /**
     * show loading
     * @param {String} content
     */
    $.weui.loading = function () {
        var content = arguments.length <= 0 || arguments[0] === undefined ? 'loading...' : arguments[0];

        var html = '<div class="weui_loading_toast">\n        <div class="weui_mask_transparent"></div>\n        <div class="weui_toast">\n            <div class="weui_loading">\n                <div class="weui_loading_leaf weui_loading_leaf_0"></div>\n                <div class="weui_loading_leaf weui_loading_leaf_1"></div>\n                <div class="weui_loading_leaf weui_loading_leaf_2"></div>\n                <div class="weui_loading_leaf weui_loading_leaf_3"></div>\n                <div class="weui_loading_leaf weui_loading_leaf_4"></div>\n                <div class="weui_loading_leaf weui_loading_leaf_5"></div>\n                <div class="weui_loading_leaf weui_loading_leaf_6"></div>\n                <div class="weui_loading_leaf weui_loading_leaf_7"></div>\n                <div class="weui_loading_leaf weui_loading_leaf_8"></div>\n                <div class="weui_loading_leaf weui_loading_leaf_9"></div>\n                <div class="weui_loading_leaf weui_loading_leaf_10"></div>\n                <div class="weui_loading_leaf weui_loading_leaf_11"></div>\n            </div>\n            <p class="weui_toast_content">' + content + '</p>\n        </div>\n    </div>';
        $loading = $(html);
        $('body').append($loading);
    };

    /**
     * hide loading
     */
    $.weui.hideLoading = function () {
        $loading && $loading.remove();
        $loading = null;
    };
})($);
'use strict';

(function ($) {
    $.fn.progress = function (options) {
        var _this = this;

        options = $.extend({
            value: 0
        }, options);
        if (options.value < 0) {
            options.value = 0;
        }

        if (options.value > 100) {
            options.value = 100;
        }

        var $progress = this.find('.weui_progress_inner_bar');
        if ($progress.length === 0) {
            var opr = typeof options.onClick === 'function' ? '<a href="javascript:;" class="weui_progress_opr">\n                    <i class="weui_icon_cancel"></i>\n                </a>' : '';
            var html = '<div class="weui_progress">\n                <div class="weui_progress_bar">\n                    <div class="weui_progress_inner_bar" style="width: ' + options.value + '%;"></div>\n                </div>\n                ' + opr + '\n            </div>';
            if (typeof options.onClick === 'function') {
                this.on('click', '.weui_progress_opr', function () {
                    options.onClick.call(_this);
                });
            }
            return this.html(html);
        }

        //return $progress.animate({
        //    width: `${options.value}%`
        //}, 100);
        return $progress.width(options.value + '%');
    };
})($);
"use strict";

(function ($) {
    $.fn.searchBar = function (options) {
        options = $.extend({
            focusingClass: 'weui_search_focusing',
            searchText: "搜索",
            cancelText: "取消"
        }, options);

        var html = "<div class=\"weui_search_bar\">\n                    <form class=\"weui_search_outer\">\n                        <div class=\"weui_search_inner\">\n                            <i class=\"weui_icon_search\"></i>\n                            <input type=\"search\" class=\"weui_search_input\" id=\"weui_search_input\" placeholder=\"" + options.searchText + "\" required/>\n                            <a href=\"javascript:\" class=\"weui_icon_clear\"></a>\n                        </div>\n                        <label for=\"weui_search_input\" class=\"weui_search_text\">\n                            <i class=\"weui_icon_search\"></i>\n                            <span>" + options.searchText + "</span>\n                        </label>\n                    </form>\n                    <a href=\"javascript:\" class=\"weui_search_cancel\">" + options.cancelText + "</a>\n                </div>";

        var $search = $(html);
        this.append($search);

        var $searchBar = this.find('.weui_search_bar');
        var $searchText = this.find('.weui_search_text');
        var $searchInput = this.find('.weui_search_input');

        this.on('focus', '#weui_search_input', function () {
            $searchText.hide();
            $searchBar.addClass(options.focusingClass);
            bindEvent($searchInput, 'onfocus', options);
        }).on('blur', '#weui_search_input', function () {
            $searchBar.removeClass(options.focusingClass);
            !!$(this).val() ? $searchText.hide() : $searchText.show();
            bindEvent($searchInput, 'onblur', options);
        }).on('touchend', '.weui_search_cancel', function () {
            $searchInput.val('');
            bindEvent($searchInput, 'oncancel', options);
        }).on('touchend', '.weui_icon_clear', function (e) {
            //阻止默认动作
            e.preventDefault();
            $searchInput.val('');
            if (document.activeElement.id != 'search_input') {
                $searchInput.trigger('focus');
            }
            bindEvent($searchInput, 'onclear', options);
        }).on('input', '.weui_search_input', function () {
            bindEvent($searchInput, 'input', options);
        }).on('submit', '.weui_search_outer', function () {
            if (typeof options.onsubmit == 'function') {
                bindEvent($searchInput, 'onsubmit', options);
                return false;
            }
        });

        function bindEvent(target, event, options) {
            if (typeof options[event] == 'function') {
                var value = $(target).val();
                options[event].call(target, value);
            }
        }
    };
})($);
'use strict';

(function ($) {
    var oldFnTab = $.fn.tab;
    $.fn.tab = function (options) {
        options = $.extend({
            defaultIndex: 0,
            activeClass: 'weui_bar_item_on',
            onToggle: $.noop
        }, options);
        var $tabbarItems = this.find('.weui_tabbar_item, .weui_navbar_item');
        var $tabBdItems = this.find('.weui_tab_bd_item');

        this.toggle = function (index) {
            var $defaultTabbarItem = $tabbarItems.eq(index);
            $defaultTabbarItem.addClass(options.activeClass).siblings().removeClass(options.activeClass);

            var $defaultTabBdItem = $tabBdItems.eq(index);
            $defaultTabBdItem.show().siblings().hide();

            options.onToggle(index);
        };
        var self = this;

        this.on('click', '.weui_tabbar_item, .weui_navbar_item', function (e) {
            var index = $(this).index();
            self.toggle(index);
        });

        this.toggle(options.defaultIndex);

        return this;
    };
    $.fn.tab.noConflict = function () {
        return oldFnTab;
    };
})($);
'use strict';

(function ($) {

    /**
     * show toast
     * @param {String} content
     * @param {Object|Number} [options]
     */
    $.weui.toast = function () {
        var content = arguments.length <= 0 || arguments[0] === undefined ? 'toast' : arguments[0];
        var options = arguments[1];


        if (typeof options === 'number') {
            options = {
                duration: options
            };
        }

        if (typeof options === 'function') {
            options = {
                callback: options
            };
        }

        options = $.extend({
            duration: 3000,
            callback: $.noop
        }, options);

        var html = '<div>\n            <div class="weui_mask_transparent"></div>\n            <div class="weui_toast">\n                <i class="weui_icon_toast"></i>\n                <p class="weui_toast_content">' + content + '</p>\n            </div>\n        </div>';
        var $toast = $(html);
        $('body').append($toast);

        setTimeout(function () {
            $toast.remove();
            $toast = null;
            options.callback();
        }, options.duration);
    };
})($);
'use strict';

(function ($) {
    var oldFnUploader = $.fn.uploader;

    $.fn.uploader = function (options) {
        var _this = this;

        options = $.extend({
            title: '图片上传',
            maxCount: 4,
            compress: true,
            maxWidth: 500,
            auto: true,
            field: 'file',
            url: '/upload.php',
            method: 'POST',
            accept: ['image/jpg', 'image/jpeg', 'image/png', 'image/gif'],
            headers: {},

            // event
            onChange: $.noop, // alias `onAddedFile`
            onAddedFile: $.noop,
            onRemovedfile: $.noop,
            onError: $.noop,
            onSuccess: $.noop,
            onComplete: $.noop

        }, options);

        var html = '<div class="weui_uploader">\n                        <div class="weui_uploader_hd weui_cell">\n                            <div class="weui_cell_bd weui_cell_primary">' + options.title + '</div>\n                            <div class="weui_cell_ft">0/' + options.maxCount + '</div>\n                        </div>\n                        <div class="weui_uploader_bd">\n                            <ul class="weui_uploader_files">\n                            </ul>\n                            <div class="weui_uploader_input_wrp">\n                                <input class="weui_uploader_input" type="file" accept="' + options.accept.join(',') + '">\n                            </div>\n                        </div>\n                    </div>';
        this.html(html);

        var $uploader = this;
        var $files = this.find('.weui_uploader_files');
        var $file = this.find('.weui_uploader_input');
        var blobs = [];

        /**
         * dataURI to blob, ref to https://gist.github.com/fupslot/5015897
         * @param dataURI
         */
        function dataURItoBlob(dataURI) {
            var byteString = atob(dataURI.split(',')[1]);
            var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
            var ab = new ArrayBuffer(byteString.length);
            var ia = new Uint8Array(ab);
            for (var i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }
            return new Blob([ab], { type: mimeString });
        }

        /**
         * error
         */
        function error(index) {
            var $preview = $files.find('.weui_uploader_file').eq(index);
            $preview.addClass('weui_uploader_status');
            $preview.html('<div class="weui_uploader_status_content"><i class="weui_icon_warn"></i></div>');
        }

        /**
         * success
         */
        function success(index) {
            var $preview = $files.find('.weui_uploader_file').eq(index);
            $preview.removeClass('weui_uploader_status');
            $preview.html('');
        }

        /**
         * update
         * @param msg
         */
        function update(msg) {
            var $preview = $files.find('.weui_uploader_file').last();
            $preview.addClass('weui_uploader_status');
            $preview.html('<div class="weui_uploader_status_content">' + msg + '</div>');
        }

        /**
         * 上传
         */
        function upload(file, index) {
            var fd = new FormData();
            fd.append(options.field, file.blob, file.name);
            $.ajax({
                type: options.method,
                url: options.url,
                data: fd,
                processData: false,
                contentType: false
            }).success(function (res) {
                success(index);
                options.onSuccess(res);
            }).error(function (err) {
                error(index);
                options.onError(err);
            }).always(function () {
                options.onComplete();
            });
        }

        $file.on('change', function (event) {
            var files = event.target.files;

            if (files.length === 0) {
                return;
            }

            if (blobs.length >= options.maxCount) {
                return;
            }

            $.each(files, function (idx, file) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    var img = new Image();
                    img.onload = function () {
                        // 不要超出最大宽度
                        var w = options.compress ? Math.min(options.maxWidth, img.width) : img.width;
                        // 高度按比例计算
                        var h = img.height * (w / img.width);
                        var canvas = document.createElement('canvas');
                        var ctx = canvas.getContext('2d');
                        // 设置 canvas 的宽度和高度
                        canvas.width = w;
                        canvas.height = h;

                        var iphone = navigator.userAgent.match(/iPhone OS ([^\s]*)/);
                        if (iphone && iphone[1].substr(0, 1) == 7) {
                            if (img.width == 3264 && img.height == 2448) {
                                // IOS7的拍照或选照片会被莫名地压缩，所以画板要height要*2
                                ctx.drawImage(img, 0, 0, w, h * 2);
                            } else {
                                ctx.drawImage(img, 0, 0, w, h);
                            }
                        } else {
                            ctx.drawImage(img, 0, 0, w, h);
                        }

                        var dataURL = canvas.toDataURL();
                        var blob = dataURItoBlob(dataURL);
                        blobs.push({ name: file.name, blob: blob });
                        var blobUrl = URL.createObjectURL(blob);

                        $files.append('<li class="weui_uploader_file " style="background-image:url(' + blobUrl + ')"></li>');
                        $uploader.find('.weui_uploader_hd .weui_cell_ft').text(blobs.length + '/' + options.maxCount);

                        // trigger onAddedfile event
                        options.onAddedFile({
                            lastModified: file.lastModified,
                            lastModifiedDate: file.lastModifiedDate,
                            name: file.name,
                            size: file.size,
                            type: file.type,
                            data: dataURL, // rename to `dataURL`, data will be remove later
                            dataURL: dataURL
                        });

                        // 如果是自动上传
                        if (options.auto) {
                            upload({ name: file.name, blob: blob }, blobs.length - 1);
                        }

                        // 如果数量达到最大, 隐藏起选择文件按钮
                        if (blobs.length >= options.maxCount) {
                            $uploader.find('.weui_uploader_input_wrp').hide();
                        }
                    };

                    img.src = e.target.result;
                };
                reader.readAsDataURL(file);
            });
        });

        this.on('click', '.weui_uploader_file', function () {
            $.weui.confirm('确定删除该图片?', function () {
                var index = $(_this).index();
                _this.remove(index);
            });
        });

        /**
         * 主动调用上传
         */
        this.upload = function () {
            // 逐个上传
            blobs.map(upload);
        };

        /**
         * 删除第 ${index} 张图片
         * @param index
         */
        this.remove = function (index) {
            var $preview = $files.find('.weui_uploader_file').eq(index);
            $preview.remove();
            blobs.splice(index, 1);
            options.onRemovedfile(index);

            // 如果数量达到最大, 隐藏起选择文件按钮
            if (blobs.length < options.maxCount) {
                $uploader.find('.weui_uploader_input_wrp').show();
            }
        };

        return this;
    };
    $.fn.uploader.noConflict = function () {
        return oldFnUploader;
    };
})($);