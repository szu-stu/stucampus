from datetime import datetime

from django.db import models
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from stucampus.account.models import LogInfor
from stucampus.utils import get_client_ip


def account_signin(request, email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        return False
    else:
        login(request, user)
        log_infor = LogInfor.objects.create(student=user.student,
                                            login_ip=get_client_ip(request))
    return True


def account_signup(request, cleaned_data):
    email = cleaned_data['email']
    password = cleaned_data['password']
    new_user = User.objects.create_user(email, email, password)
    screen_name, email_domain = email.split('@')
    student = Student.objects.create(user=new_user, screen_name=screen_name)


def account_update(request, user, cleaned_data):
    user.student.true_name = cleaned_data['true_name']
    user.student.college = cleaned_data['college']
    user.student.screen_name = cleaned_data['screen_name']
    user.student.is_male = cleaned_data['is_male']
    user.student.mphone_num = cleaned_data['mphone_num']
    user.student.mphone_short_num = cleaned_data['mphone_short_num']
    user.student.student_id = cleaned_data['student_id']
    user.student.szucard = cleaned_data['szucard']
    birthday = data['birthday']
    if len(birthday) > 0:
        user.student.birthday = datetime.strptime(birthday, '%Y-%m-%d')
    user.student.save()
