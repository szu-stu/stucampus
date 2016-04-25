#-*- coding: utf-8
from django.db import models
from django.utils.text import capfirst
from django.core import exceptions

from DjangoUeditor.models import UEditorField

from stucampus.custom.form_field import MultiSelectFormField
from stucampus.custom.qiniu import upload_content_img_to_qiniu,upload_img


class MultiSelectField(models.Field):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "CharField"

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def _get_FIELD_display(self, field):
        value = getattr(self, field.attname)
        choicedict = dict(field.choices)

    def formfield(self, **kwargs):
        # don't call super, as that overrides default widget if it has choices
        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name), 
                    'help_text': self.help_text,
                    'choices':self.choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_db_prep_value(self, value, connection, prepared=False):
        if isinstance(value, basestring):
            return value
        elif isinstance(value, list):
            return ",".join(value)
      
    def to_python(self, value):
        if isinstance(value, list):
            return value
        return value.split(",")

    def contribute_to_class(self, cls, name):
        super(MultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            func = lambda self, fieldname = name, choicedict = dict(
                self.choices): ",".join(
                    [choicedict.get(value,value) \
                    for value in getattr(self,fieldname)])
            setattr(cls, 'get_%s_display' % self.name, func)

    def validate(self, value, model_instance):
        arr_choices = self.get_choices_selected(self.get_choices_default())
        for opt_select in value:
            if (opt_select not in arr_choices): 
                raise exceptions.ValidationError( \
                    self.error_messages['invalid_choice'] % value)    

    def get_choices_selected(self, arr_choices=""):
        if not arr_choices:
            return False
        l = []
        for choice_selected in arr_choices:
            l.append(choice_selected[0])
        return l

class QiniuImageField(models.ImageField):
    '''
        @author:jimczj
        e-mail:jimczj@gmail.com
        将ImageField里面的图片上传到七牛，保存到数据库的时候自动执行
    '''


    def to_python(self, value):
        if not value:
            return value
        
        upload_img(str(value))
        return value

class QiniuUEditorField(UEditorField):
    '''
        @author:jimczj
        e-mail:jimczj@gmail.com
        将djangoUeditor里面的图片上传到七牛，保存到数据库的时候自动执行
    '''


    def to_python(self, value):
        if not value:
            return value

        return upload_content_img_to_qiniu(value)



