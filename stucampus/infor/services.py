from django.shortcuts import render, get_object_or_404

from stucampus.infor.models import Infor
from stucampus.organization.models import Organization


def post_infor(request, cleaned_data):
    title = cleaned_data['title']
    content = cleaned_data['content']
    organization_id = cleaned_data['organization_id']
    author = request.user.student
    organization = get_object_or_404(Organization, id=organization_id)
    Infor.objects.create(title=title, content=content,
                         author=author, organization=organization)


def infor_update(infor, cleaned_data):
    infor.title = cleaned_data['title']
    infor.content = cleaned_data['content']
    infor.organization_id = cleaned_data['organization_id']
    infor.save()
