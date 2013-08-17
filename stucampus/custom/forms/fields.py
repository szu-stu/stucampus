#-*- coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _, ungettext_lazy


ENTER_A_NUMBER = u'请输入数字'


class CharField(forms.CharField):
    default_error_messages = {
        'required': _(u'不能为空'),
    }


class IntegerField(forms.IntegerField):
    default_error_messages = {
        'invalid': _(ENTER_A_NUMBER),
    }


class FloatField(forms.FloatField):
    default_error_messages = {
        'invalid': _(ENTER_A_NUMBER),
    }


class DecimalField(IntegerField):
    default_error_messages = {
        'invalid': _(ENTER_A_NUMBER),
        'max_digits': ungettext_lazy(
            # 'Ensure that there are no more than %(max)s digit in total.',
            '请确保输入的值不大于 %(max)s'
            # 'Ensure that there are no more than %(max)s digits in total.',
            '请确保输入的值不大于 %(max)s'
            # 'max',
            '最大'),
        'max_decimal_places': ungettext_lazy(
            # 'Ensure that there are no more than %(max)s decimal place.',
            '请确保输入的值不大于 %(max)s'
            # 'Ensure that there are no more than %(max)s decimal places.',
            '请确保输入的值不大于 %(max)s'
            # 'max',
            '最大'),
        'max_whole_digits': ungettext_lazy(
            # 'Ensure that there are no more than %(max)s digit before the decimal point.',
            '请确保输入的值不大于 %(max)s'
            # 'Ensure that there are no more than %(max)s digits before the decimal point.',
            '请确保输入的值不大于 %(max)s'
            # 'max',
            '最大'),
    }


class DateField(forms.DateField):
    default_error_messages = {
        'invalid': _(u'请输入合法日期'),
    }


class TimeField(forms.TimeField):
    default_error_messages = {
        'invalid': _(u'请输入合法时间'),
    }


class DateTimeField(forms.DateTimeField):
    default_error_messages = {
        'invalid': _(u'请输入合法日期/时间'),
    }


class RegexField(forms.RegexField):
    pass


class EmailField(forms.EmailField):
    default_error_messages = {
        'invalid': _(u'请输入合法邮箱地址')
    }


class FileField(forms.FileField):
    default_error_messages = {
        # 'invalid': _("No file was submitted. Check the encoding type on the form."),
        'invalid': _(u'找不到文件, 请重新上传文件.'),
        'missing': _(u'找不到文件, 请重新上传文件.'),
        'empty': _(u'文件为空, 上传失败'),
        'max_length': ungettext_lazy(
            '文件需小于 %(max)d 字节, (您上传的文件大小为 %(length)d).',
            '文件需小于 %(max)d 字节, (您上传的文件大小为 %(length)d).',
            '最大'
        ),
        'contradiction': _('Please either submit a file or check '
                           'the clear checkbox, not both.')
    }


class ImageField(forms.ImageField):
    default_error_messages = {
        'invalid_image': _(u'您上传的图片不合法, 请重新上传'),
    }


class URLField(forms.URLField):
    default_error_messages = {
        'invalid': _(u'请输入合法 URL'),
    }


class BooleanField(forms.BooleanField):
    pass


class NullBooleanField(BooleanField):
    pass


class ChoiceField(forms.ChoiceField):
    default_error_messages = {
        'invalid_choice': _(u'请选择合法选项, %(value)s 不是合法选项'),
    }


class TypedChoiceField(ChoiceField):
    pass


class MultipleChoiceField(forms.MultipleChoiceField):
    default_error_messages = {
        'invalid_choice': _(u'请选择合法选项, %(value)s 不是合法选项'),
        'invalid_list': _(u'Enter a list of values'),
    }


class TypedMultipleChoiceField(MultipleChoiceField):
    pass


class ComboField(forms.ComboField):
    pass


class MultiValueField(forms.MultiValueField):
    default_error_messages = {
        'invalid': _(u'Enter a list of values'),
        'incomplete': _(u'Enter a complete value'),
    }


class FilePathField(ChoiceField):
    pass


class SplitDateTimeField(MultiValueField):
    pass


class IPAddressField(CharField):
    pass


class GenericIPAddressField(CharField):
    pass


class SlugField(CharField):
    pass