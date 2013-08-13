from django import forms
from django.utils.translation import ugettext_lazy as _, ungettext_lazy

this_field_is_required = 'todo : translate it into chinese'

class IntegerField(forms.IntegerField):
    default_error_messages = { \
        'invalid':_('chinese Enter a whole number'), \
        'required':_( this_field_is_required ), \
        }

class FloatField(forms.FloatField):
    default_error_messages = { \
        'invalid':_('Enter a numer.'),\
        'required':-( this_field_is_required ),\
        }

class DateField(form.DateField):
    default_error_messages = { \
        'invalid'=_('Enter a valid date.'),\
        }

class TimeField(forms.TimeField):
    default_error_messages = { \
        'invalid':_('Enter a valid time'),\
        }

class DateTimeField(forms.DateTimeField):
    default_error_messages = { \
        'invalid':_('Enter a valid date/time.'),\
        }

class EmailField(forms.EmailField):
    default_error_messages = { \
        'required':_( this_field_is_required ), \
        }

class FileField(forms.FileField):
    default_error_messages = { \
        'invalid':_('chinese No file was submitted.Check the encoding type on the forms.'),\
        'missing':_('chinese No file wa submitted'),\
        'empty':_('chinese The submitted file is empty'),\

        'max_length':ungettext_lazy(\
            'chinese Ensure this filename has at most %(max)d character (it has %(length)d).',\
            'chineseEnsure this filename has at most %(max)d characters (it has %(length)d.',\
            'max'),\

        'contradiction':_('chinesePlease either submit a file or check the clear checkbox, not both.')\
        }

class ImageField(forms.ImageField):
    default_error_messages = {\
        'invalid_image':_('chineseUpload a valid image. The file you uploaded was either not an image or a corrupted image.'),\
        }

class URLField(forms.URLField):
    default_error_messages = {\
        'invalid':_('chineseEnter a valid URL'),\
        }

class ChoiceField(forms.ChoiceField):
    default_error_messages = {\
        'invalid_choice':_('chineseSelect a valid choice, %(value)s is not one of the available choices'),\
        }

class MultipleChoiceField(forms.MultipleChoiceField):
    default_error_messages = { \
        'invalid_choice':-('chineseSelect a valid choice. %(value)s is not one of the available choices.'),\
        'invalid_list':_('chineseEnter a list of values'),\
        }

class MultiValueField(forms.MultiValueField):
    default_error_messages = { \
        'invalid':_('chineseEnter a list of values'),\
        'incomplete':_('chineseEnter a complete value'),\
        }

