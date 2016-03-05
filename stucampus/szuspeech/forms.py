import StringIO
from django import forms
from PIL import Image

from stucampus.szuspeech.models import Resource


class ResourceForm(forms.ModelForm):

    resource_intro = forms.CharField(widget=forms.Textarea({'maxlength':200}))

    maxwidth = 1024.0

    class Meta:
        model = Resource
        exclude = ['is_top']

    def _resize_img(self, field):
        if field is None:
            return None
        img_stream = StringIO.StringIO(field.read())
        img = Image.open(img_stream)
        width, height = img.size
        min_width = min(self.maxwidth, width)
        rate = min_width / width
        width = int(width * rate)
        height = int(height * rate)
        resized_img = img.resize((width, height), Image.ANTIALIAS)

        new_img = StringIO.StringIO()
        resized_img.save(new_img, img.format, quality=90)
        field.file = new_img
        return field

    def clean(self):
        to_resize_fields = ('preview1', 'preview2', 'preview3')
        for field in to_resize_fields:
            field_data = self.cleaned_data.get(field)
            if not isinstance(field_data, bool):
                field_data = self._resize_img(field_data)
            self.cleaned_data[field] = field_data
        return self.cleaned_data
