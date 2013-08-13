from django.db import models
from stucampus.stucampus_custom import forms 

class CharField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CharField}
        defaults.update(kwargs)
        return super(CharField, self).formfield(**defaults)

class IntegerField(models.IntegerField):
    def formfield(self, **kwargs):
        defaults = {'form_class': stucampus_FormField.IntegerField}
        defaults.update(kwargs)
        return super(IntegerField, self).formfield(**defaults)

class FloatField(models.FloatField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.FloatField}
        defaults.update(kwargs)
        return super(FloatField, self).formfield(**defaults)

class DateField(models.DateField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.DateField}
        defaults.update(kwargs)
        return super(DateField, self).formfield(**defaults)
    
class TimeField(models.TimeField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.TimeField}
        defaults.update(kwargs)
        return super(TimeField, self).formfield(**defaults)

class DateTimeField(models.DateTimeField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.DateTimeField}
        defaults.update(kwargs)
        return super(DateTimeField, self).formfield(**defaults)

class EmailField(models.EmailField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.EmailField}
        defaults.update(kwargs)
        return super(EmailField, self).formfield(**defaults)
class FileField(models.FileField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.FileField}
        defaults.update(kwargs)
        return super(FileField, self).formfield(**defaults)

class ImageField(models.ImageField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.ImageField}
        defaults.update(kwargs)
        return super(ImageField, self).formfield(**defaults)

class URLField(models.URLField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.URLField}
        defaults.update(kwargs)
        return super(URLField, self).formfield(**defaults)

class CharField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CharField}
        defaults.update(kwargs)
        return super(CharField, self).formfield(**defaults)

class BooleanField(models.BooleanField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.BooleanField}
        defaults.update(kwargs)
        return super(BooleanField, self).formfield(**defaults)



