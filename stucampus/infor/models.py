from django.db import models

from stucampus.account.models import Student
from stucampus.organization.models import Organization


class Infor(models.Model):

    class Meta:
        permissions = (
            ('infors_list', 'List all informations'),
            ('infor_show', 'Show an informations'),
            ('infor_create', 'Create an information'),
            ('infor_edit', 'Edit an information'),
            ('infor_del', 'Delete an information')
        )

    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(Student)
    organization = models.ForeignKey(Organization)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    count = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
