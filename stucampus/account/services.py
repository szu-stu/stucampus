from datetime import datetime

from django.db import models
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def account_signup(request, cleaned_data):
    email = cleaned_data['email']
    password = cleaned_data['password']
    new_user = User.objects.create_user(email, email, password)
    screen_name = email.split('@', 1)
    student = Student.objects.create(user=new_user, screen_name=screen_name)
