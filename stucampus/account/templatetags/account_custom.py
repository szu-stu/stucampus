from hashlib import md5

from django import template
from django.contrib.auth.models import User


register = template.Library()


@register.filter(name='user_avatar')
def user_avatar(user):
    if isinstance(user, User):
        email = user.email
        hashed_email = md5(email).hexdigest()
        return hashed_email
    else:
        return None