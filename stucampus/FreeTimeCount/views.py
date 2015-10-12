

from django.template.response import TemplateResponse

from stucampus.FreeTimeCount import functions
from stucampus.account.permission import check_perms

# Create your views here.

@check_perms('FreeTimeCount.usable')
def index(request):
	response = TemplateResponse(request, 'FreeTimeCount/index.html', {})
	return response

@check_perms('FreeTimeCount.usable')
def date(request):

	return date_function(request)

@check_perms('FreeTimeCount.usable')
def distribute(request):

	return distribute_function(request)

@check_perms('FreeTimeCount.usable')
def member(request):
	return member_function(request)

@check_perms('FreeTimeCount.usable')
def insert(request):
	return insert_function(request)
