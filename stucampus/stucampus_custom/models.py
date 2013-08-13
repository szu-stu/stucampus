from django.db import models
from stucam.stucampus_core import stucampus_FormField

class IntegerField(models.IntegerField):
    def formfield(self, **kwargs):
        defaults = {'form_class': stucampus_FormField.IntegerField}
        defaults.update(kwargs)
        return super(IntegerField, self).formfield(**defaults)
