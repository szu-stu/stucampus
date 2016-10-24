from datetime import datetime

from django.db import models
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from stucampus.account.models import Student


def account_signup(request, cleaned_data):
    email = cleaned_data['email']
    password = cleaned_data['password']
    new_user = User.objects.create_user(email, email, password)
    screen_name, email_domain = email.rsplit('@', 1)
    student = Student.objects.create(user=new_user, screen_name=screen_name, true_name=request.session['szu_name'], job_id=request.session['szu_no'])
