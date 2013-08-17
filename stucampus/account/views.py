from django.http import HttpResponse
from django.shortcuts import render

from stucampus.account.services import validate_user
from stucampus.utils import render_json


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'account/signin.html')
    elif request.method == 'POST':
        data = request.POST
        email = data['email']
        passwd = data['password']
        validated = validate_user(email, passwd)
        if validated:
            context = {'success': True}
        else:
            context = {'success': False}
        return render_json(context)
