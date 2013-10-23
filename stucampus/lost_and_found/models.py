from django.forms import ModelForm
import datetime
import django.db.models

from stucampus.custom import models


class Message(django.db.models.Model):

    # TODO: translate the second value of every tuple to chinese
    CATEGORY_CHOICES = (
        ('phone', 'phone'),
        ('bag', 'bag'),
        ('idcard', 'idcard'),
        ('bike', 'bike'),
    )

    MESSAGE_TYPE = ((True, u'find item'), (False, u'find owner'))

    message_type = models.BooleanField(default=True, choices=MESSAGE_TYPE)
    item_name = models.CharField(max_length=40,
                                 verbose_name='item name in chinese')
    description = models.CharField(max_length=300)
    picture_file = models.ImageField(upload_to='lost_and_found',
                                     blank=True)
    published_date = models.DateField(auto_now_add=True) 
    place = models.CharField(max_length=50)

    category = models.ChoiceField(max_length=20, choices=CATEGORY_CHOICES)

    publisher_name = models.CharField(max_length=20)
    contact_way = models.CharField(max_length=30)

    is_solved = models.BooleanField(default=False)

    def how_many_days_since_published(self):
        return (datetime.date.today() - published_date).days


class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ('published_date', 'is_solved')
