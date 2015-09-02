#-*- coding: utf-8 -*-
from django import forms

from stucampus.minivideo.models import Resource

class SignUpForm(forms.ModelForm):

    team_psw = forms.CharField(
        label=(u'team_psw'), max_length=30,
        widget=forms.PasswordInput(),
        error_messages={
            'required': (u'此字段必填'),
            'max_length': (u'密码长度不得超过30')
        }
    )
    
    confirm = forms.CharField(
        label=(u'密码确认'), max_length=30,
        widget=forms.PasswordInput(),
        error_messages={
            'required': (u'此字段必填'),
            'max_length': (u'密码长度不得超过30')
        }
    )

    def clean_team_captain_stuno(self):
        stuno = self.cleaned_data.get('team_captain_stuno')
        if Resource.objects.filter(team_captain_stuno=stuno).exists():
            raise forms.ValidationError((u'该学号已报名'))
        return stuno

    def clean_confirm(self):
        team_psw = self.cleaned_data.get('team_psw')
        confirm = self.cleaned_data.get('confirm')
        if not team_psw == confirm:
            raise forms.ValidationError((u'前后输入密码不一致'))
        return confirm

    class Meta:
         model = Resource
         exclude = ('video_cover', 'video_name', 'video_intro', 'video_link', 'votes', 'has_verified')

class CommitForm(forms.ModelForm):

    video_intro = forms.CharField(
        widget=forms.Textarea({'maxlength':200}),
        )

    confirm = forms.CharField(
        label=(u'密码'), max_length=30,
        widget=forms.PasswordInput(),
        error_messages={
            'required': (u'此字段必填'),
            'max_length': (u'密码长度不得超过30')
        }
    )

    def clean_confirm(self):
        stuno = self.cleaned_data.get('team_captain_stuno')
        resource = Resource.objects.get(team_captain_stuno=stuno)
        team_psw = resource.team_psw
        confirm = self.cleaned_data.get('confirm')
        if not team_psw == confirm:
            raise forms.ValidationError((u'密码错误'))
        return confirm

    def clean_video_cover(self):
        cover = self.cleaned_data.get('video_cover')
        if cover.size > 524288:
            raise forms.ValidationError((u'请上传小于512KB的图片'))
        return cover

    class Meta:
         model = Resource
         exclude = ('team_captain', 'team_captain_phone', 
             'team_captain_college',
            'team_members1_name', 'team_members1_id',
            'team_members2_name', 'team_members2_id',
            'team_members3_name', 'team_members3_id', 
            'team_members4_name', 'team_members4_id', 
            'team_members5_name', 'team_members5_id',
            'team_psw', 'votes', 'has_verified')

       
class loginForm(forms.ModelForm):

    confirm = forms.CharField(
        label=(u'密码'), max_length=30,
        widget=forms.PasswordInput(),
        error_messages={
            'required': (u'这个字段是必填项。'),
            'max_length': (u'密码长度不得超过30')
        }
    )

    def clean_confirm(self):
        stuno = self.cleaned_data.get('team_captain_stuno')
        if not Resource.objects.filter(team_captain_stuno=stuno).exists():
            raise forms.ValidationError((u'该队长学号不存在'))
        resource = Resource.objects.get(team_captain_stuno=stuno)
        team_psw = resource.team_psw
        confirm = self.cleaned_data.get('confirm')
        if not team_psw == confirm:
            raise forms.ValidationError((u'密码错误'))
        return confirm

    class Meta:
        model = Resource
        exclude = ('team_captain', 'team_captain_phone', 
             'team_captain_college',
            'team_members1_name', 'team_members1_id',
            'team_members2_name', 'team_members2_id',
            'team_members3_name', 'team_members3_id', 
            'team_members4_name', 'team_members4_id', 
            'team_members5_name', 'team_members5_id',
            'team_psw', 'votes', 'has_verified',
            'video_cover', 'video_name', 'video_intro',
             'video_link', 'votes', 'has_verified')