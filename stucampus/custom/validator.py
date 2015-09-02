#-*- coding:utf-8 -*-
from django.core.exceptions import ValidationError


def validate_file_extension(valid_file_extension):
    ''' used by models.FileField '''
    if not isinstance(valid_file_extension, (dict, list, tuple)):
        valid_file_extension = [valid_file_extension]
    def validate(value):
        ''' function do the actual validate work '''
        for extension in valid_file_extension:
            if value.name.endswith(extension):
                return
        raise ValidationError(u'不能上传该格式的文件')
    return validate
