from django.shortcuts import render, get_object_or_404

from stucampus.infor.models import Infor
from stucampus.organization.models import Organization


def post_infor(request, cleaned_data):
    title = cleaned_data['title']
    content = cleaned_data['content']
    organization = cleaned_data['organization']
    author = request.user.student
    Infor.objects.create(title=title, content=content,
                         author=author, organization=organization)
