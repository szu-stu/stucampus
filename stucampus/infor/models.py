from django.db import models

from stucampus.account.models import Student
from stucampus.organization.models import Organization


class Infor(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(Student)
    organization = models.ForeignKey(Organization)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    count = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
