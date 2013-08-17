from django.forms import ModelForm
import datetime
import django.db.models

from stucampus.custom import models


class Message(django.db.models.Model):
    not_seeking_item_but_owner = models.BooleanField()

    item_name = models.CharField(max_length=40,
                                 verbose_name='item name in chinese')
    description = models.CharField(max_length=300)
    picture_file = models.ImageField(upload_to='lostAndFind')
    published_date = models.DateField(auto_now_add=True)
    place = models.CharField(max_length=50)
    # TODO: translte the second value of every tuple to chinese
    KIND_CHOICES = (
        ('phone', 'phone'),
        ('bag', 'bag'),
        ('idcard', 'idcard'),
        ('bike', 'bike'),
    )
    kind = models.ChoiceField(max_length=20, choices=KIND_CHOICES)

    publisher_name = models.CharField(max_length=20)
    contact_way = models.CharField(max_length=30)

    is_solved = models.BooleanField(default=False)

    def how_many_days_since_published(self):
        return (datetime.date.today() - published_date).days

    def __unicode__(self):
        return self.item_name


class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ('published_date', 'is_solved')
