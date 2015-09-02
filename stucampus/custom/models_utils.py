#-*- coding: utf-8 -*-
import os

def file_save_path(instance, filename):
    ''' indicate saving path of uploaded file
        used in model.FileField ,ImageField,etc.
    '''
    return os.path.join(instance.editor.true_name, filename)

