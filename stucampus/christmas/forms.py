#coding:utf-8
from django import forms
from .models import ExchangeGift, Gift, GiftSystem_user, GivenGift, ChangeResult
from django.core.exceptions import ValidationError
import re

class GivenForm(forms.ModelForm):
    givenPhone = forms.CharField(label="收礼人电话", max_length=11, required=True, error_messages={"required": u"给定人电话为必填项"})
    givenAdress = forms.CharField(label="收礼人地址", max_length=1000, required=True, error_messages={"required": u"地址为必须项"})
    givenPerson = forms.CharField(label="收礼人姓名", max_length=100, required=True, error_messages={"required": u"给定人为必须项"})
    def clean_givenPhone(self):
        givenPhone = self.cleaned_data["givenPhone"]
        p = re.compile('^0\d{2,3}\d{7,8}$|^1[3578]\d{9}$|^147\d{8}')
        if p.match(givenPhone):
            return givenPhone
        raise ValidationError(u"手机号码格式有误")
    class Meta:
        model = GivenGift
        fields = ["givenPerson", "givenAdress", "givenPhone"]

class ExchangeForm(forms.ModelForm):
    aimGroup = forms.CharField(label="目标群体", max_length=6, required=True, error_messages={"required": u'目标群体不能为空'})
    def clean_aimGroup(self):
        aimGroup = self.cleaned_data["aimGroup"]
        if not aimGroup or not (aimGroup == "female" or aimGroup == "male" or aimGroup == "both"):
            raise ValidationError(u"赠予群体不正确")
        return aimGroup
    class Meta:
        model = ExchangeGift
        exclude = ["id", "gift"]

class GiftForm(forms.ModelForm):
    name = forms.CharField(label="礼物名称", required=True, max_length=100, error_messages={"required":u"名字不能为空"})
    isAnonymous = forms.BooleanField(label="是否匿名", required=False)
    description = forms.CharField(label="礼物描述", required=False, widget=forms.Textarea)
    type = forms.CharField(label="礼物类别", required=True, error_messages={"required": u"礼物类别不能为空"})
    def clean_type(self):
        type = self.cleaned_data["type"]
        if int(type)>12 or int(type)<1:
            raise ValidationError(u"类别选择错误")
        return type
    class Meta:
        model = Gift
        exclude = ["id", "isExchange", "own", "giftId"]#, "giftId", "own", "isExchange", "isUsed", "isGet", "isDelete"]

class UserForm(forms.ModelForm):
    wechat = forms.CharField(label="微信号", max_length=50, required=False)
    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        p = re.compile('^0\d{2,3}\d{7,8}$|^1[3578]\d{9}$|^147\d{8}')
        if p.match(phone):
            return phone
        raise ValidationError(u"手机号码格式有误")
    def clean_area(self):
        area = self.cleaned_data["area"]
        if area>'C' or area<'':
            raise ValidationError(u'居住区域选择错误')
        return area
    class Meta:
        model = GiftSystem_user
        fields = ["phone", "area", "wechat"]

class ChangeForm(forms.ModelForm):
    getGiftId = forms.CharField(label="交换结果", required=False)
    class Meta:
        model = ChangeResult
        fields = ["wangGiftType", "getGiftId", "exchangegift"]
