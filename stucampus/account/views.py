#-*- coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render

from stucampus.utils import render_json
from stucampus.account.services import validate_user
from stucampus.account.forms import SignInForm


def sign_in(request):
    if request.method == 'GET':
        form = SignInForm()
        return render(request, 'account/signin.html', {'form': form})
    elif request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            passwd = request.POST['password']
            success = validate_user(email, passwd)
            if not success:
                messages = [u'邮箱或密码错误']
        else:
            success = False
            messages = form.errors.values()
        return render_json({'success': success, 'messages': messages})
