from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from stucampus.utils import spec_json, get_client_ip
from stucampus.custom.permission import guest_or_redirect
from stucampus.account.models import Student, UserActivityLog
from stucampus.account.services import account_signup
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
            return spec_json(status='errors', messages=messages)

        user = form.get_user()
        login(request, user)
        UserActivityLog.objects.create(user=user,
                                       ip_address=get_client_ip(request),
                                       behavior="Login")
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
            return spec_json(status='errors', messages=messages)

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        account_signup(request, form.cleaned_data)
        return spec_json(status='success')


class Profile(View):
    '''View of profile'''
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'account/profile.html')


class ProfileEdit(View):
    '''View of editing profile'''
    @method_decorator(login_required)
    def get(self, request):
        college_list = Student.COLLEGE_CHOICES
        return render(request, 'account/profile-edit.html',
                      {'college_list': college_list})

    @method_decorator(login_required)
    def post(self, request):
        student = request.user.student
        form = ProfileEditForm(request.POST, instance=student)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='errors', messages=messages)
        form.save()
        return spec_json(status='success')


class Password(View):
    '''View of editing password'''
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'account/password.html')

    @method_decorator(login_required)
    def post(self, request):
        form = PasswordForm(request.POST)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='errors', messages=messages)

        current_user = request.user
        current_user.set_password(form.cleaned_data.get('new_password'))
        current_user.save()
        return spec_json(status='success')
