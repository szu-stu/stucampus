from datetime import datetime

from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from stucampus.utils import spec_json, get_client_ip, get_http_data
from stucampus.custom.permission import guest_or_redirect
from stucampus.account.models import Student
from stucampus.account.forms import SignInForm, SignUpForm
from stucampus.account.forms import ProfileEditForm, PasswordForm
from stucampus.account.services import find_by_email, is_email_exist


class SignIn(View):
    '''View of account sign in page'''
    @method_decorator(guest_or_redirect)
    def get(self, request):
        return render(request, 'account/sign-in.html')

    @method_decorator(guest_or_redirect)
    def post(self, request):
        form = SignInForm(request.POST)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='form_errors', messages=messages)

        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is None:
            return spec_json(status='user_not_valid')

        if not user.is_active:
            return spec_json(status='user_not_active')
        
        login(request, user)
        user.student.login_count = user.student.login_count + 1
        user.student.last_login_ip = get_client_ip(request)
        user.student.save()
        return spec_json(status='success')


class SignOut(View):
    '''View of account sign out page'''
    def post(self, request):
        logout(request)
        status = 'success'
        return spec_json(status)


class SignUp(View):
    '''View of account sign up page.'''
    @method_decorator(guest_or_redirect)
    def get(self, request):
        return render(request, 'account/sign-up.html')

    @method_decorator(guest_or_redirect)
    def post(self, request):
        form = SignUpForm(request.POST)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='form_errors', messages=messages)

        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']
        if not password == confirm:
            return spec_json(status='passwords_not_match')

        email_is_exist = is_email_exist(email)
        if email_is_exist:
            return spec_json(status='email_existed')

        new_user = User.objects.create_user(email, email, password)
        student = Student.objects.create(user=new_user)
        student.screen_name, email_domain = email.split('@')
        student.last_login_ip = get_client_ip(request)
        student.save()
        login(username=email, password=password)
        return spec_json(status='success')


class Profile(View):
    '''View of profile'''
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'account/profile.html')

    @method_decorator(login_required)
    def put(self, request):
        data = get_http_data(request)
        form = ProfileEditForm(data)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='form_errors', messages=messages)

        user = request.user
        user.student.true_name = data['true_name']
        user.student.college = data['college']
        user.student.screen_name = data['screen_name']
        user.student.is_male = data['is_male']
        user.student.mphone_num = data['mphone_num']
        birthday = data['birthday']
        if len(birthday) > 0:
            user.student.birthday = datetime.strptime(birthday, '%Y-%m-%d')
        user.student.mphone_short_num = data['mphone_short_num']
        user.student.student_id = data['student_id']
        user.student.szucard = data['szucard']
        user.student.save()
        return spec_json(status='success')


class ProfileEdit(View):
    '''View of editing profile'''
    @method_decorator(login_required)
    def get(self, request):
        college_list = Student.COLLEGE_CHOICES
        return render(request, 'account/profile-edit.html',
                      {'college_list': college_list})


class Password(View):
    '''View of editing password'''
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'account/password.html')

    @method_decorator(login_required)
    def put(self, request):
        data = get_http_data(request)
        form = PasswordForm(data)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='form_errors', messages=messages)

        current_user = request.user
        query_user = authenticate(username=current_user.username,
                                  password=data['current_password'])
        if query_user is None:
            return spec_json(status='wrong_password')

        if not data['new_password'] == data['confirm']:
            return spec_json(status='passwords_not_match')

        current_user.set_password(data['confirm'])
        current_user.save()
        return spec_json(status='success')
