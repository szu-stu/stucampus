from datetime import datetime

from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from stucampus.utils import spec_json, get_client_ip, get_http_data
from stucampus.custom.permission import guest_or_redirect
from stucampus.account.models import Student, LogInfor
from stucampus.account.forms import SignInForm, SignUpForm
from stucampus.account.forms import ProfileEditForm, PasswordForm


class SignIn(View):
    """Class-base view to handle account sign in request"""
    @method_decorator(guest_or_redirect)
    def get(self, request):
        return render(request, 'account/sign-in.html')

    @method_decorator(guest_or_redirect)
    def post(self, request):
        form = SignInForm(request.POST)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='form_errors', messages=messages)

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=email, password=password)
        login(request, user)
        log_infor = LogInfor.objects.create(student=user.student)
        log_infor.login_ip = get_client_ip(request)
        log_infor.save()
        return spec_json(status='success')


class SignOut(View):
    '''View of account sign out page'''
    def post(self, request):
        logout(request)
        return spec_json(status='success')


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

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        new_user = User.objects.create_user(email, email, password)
        student = Student.objects.create(user=new_user)
        student.screen_name, email_domain = email.split('@')
        student.last_login_ip = get_client_ip(request)
        student.save()
        user = authenticate(username=email, password=password)
        login(request, user)
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
        current_user.set_password(form.cleaned_data.get('new_password'))
        current_user.save()
        return spec_json(status='success')
