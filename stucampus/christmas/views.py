#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import ExchangeGift, Gift, GiftSystem_user, GivenGift, ChangeResult
from django.views.generic import View
from .forms import ExchangeForm, GiftForm, UserForm, GivenForm
import json
from login_szu import login_szu
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from stucampus.account.permission import check_perms
from django.utils.decorators import method_decorator

'''
用来判断网页是否可用时间的装饰器，但只有判定开放时间，没判定关闭时间，有需求可改
'''
def time_require(starttime="2016-12-7", endtime=""):
    def decorator(function):
        def wrapped_check(request, *args, **kwargs):
            now = datetime.now().date()
            year, month, day = starttime.split("-")   
            aimdate = datetime(int(year), int(month), int(day)).date()
            if endtime:
                year, month, day = starttime.split("-")
            enddate = datetime(int(year), int(month), int(day)).date()
            if now < aimdate:
                return render(request, 'christmas/error.html')
            if endtime:
                if now >= enddate:
                    return HttpResponse("此网页已关闭")
            return function(request, *args, **kwargs)
        return wrapped_check
    return decorator

def readRequire(function):
    def wrapped_check(request, *args, **kwargs):
        current_user = get_object_or_404(GiftSystem_user, stu_no=request.session['szu_no'])
        if not current_user.isRead:
            return HttpResponseRedirect("/christmas/read/")
        return function(request, *args, **kwargs)
    return wrapped_check


class ReadView(View):
    @login_szu
    def get(self, request):
        return render(request, "christmas/read.html")
    @login_szu
    def post(self, request):
        user = get_object_or_404(GiftSystem_user, stu_no=request.session['szu_no'])
        user.isRead = True
        user.save()
        return render(request, 'christmas/index.html', locals())
class ReadDetailView(View):
    @login_szu
    def get(self, request):
        return render(request, "christmas/readDetail.html")
    @login_szu
    def post(self, request):
        user = get_object_or_404(GiftSystem_user, stu_no=request.session['szu_no'])
        user.isRead = True
        user.save()
        return render(request, 'christmas/index.html', locals())

class ExchangeView(View):
    @login_szu
    def get(self, request):
        exchange = ExchangeForm()
        gift = GiftForm()
        current_user = GiftSystem_user.objects.get(stu_no=request.session['szu_no'])
        user = UserForm()
        return render(request, 'christmas/addExchange.html', locals())
    
    @login_szu
    def post(self, request):
        currentUser = get_object_or_404(GiftSystem_user, stu_no=request.session['szu_no'])
        gifts = Gift.objects.filter(own__stu_no=request.session['szu_no'], isDelete=False)
        if len(gifts) > 2:
            data = {"status": "full", "message": u"您的礼物数目满了噢"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        exchange = ExchangeForm(request.POST)
        gift = GiftForm(request.POST)
        user = UserForm(request.POST)
        if not currentUser.phone or not currentUser.area:
            if user.is_valid():
                phone = user.cleaned_data['phone']
                area = user.data['area']
                wechat = user.data['wechat']
            else:
                data = {"status": "error", "message": user.errors.values()}
                return HttpResponse(json.dumps(data), content_type="application/json")
            currentUser.area = area
            currentUser.phone = phone
            currentUser.wechat = wechat
            currentUser.save()
        if exchange.is_valid() and gift.is_valid():
            t = Gift.objects.create(
                name = gift.data["name"],
                type = gift.data["type"],
                description = gift.data["description"],
                isAnonymous = gift.cleaned_data["isAnonymous"],
                giftId= currentUser.area + gift.data["type"] + "{:0>5}".format(
                    len(Gift.objects.filter(own__area=currentUser.area)) + 1)
            )
            try:
                ExchangeGift.objects.create(
                    aimGroup = exchange.data["aimGroup"],
                    gift = t
                )
            except:
                t.delete()
            t.own = currentUser
            t.save()
            data = {'status': 'success', 'message': "您的礼物ID是:%s" % t.giftId}
            return HttpResponse(json.dumps(data), content_type='application/json')
        exchange_message = [i for i in exchange.errors.values()]
        gift_message = [i for i in gift.errors.values()]
        data = {"status": "error", "message": exchange_message + gift_message}
        return HttpResponse(json.dumps(data), content_type="application/json")

class GivenView(View):
    @login_szu
    def get(self, request):
        given = GivenForm()
        gift = GiftForm()
        current_user = GiftSystem_user.objects.get(stu_no=request.session['szu_no'])
        user = UserForm()
        return render(request, "christmas/addGiven.html", locals())
    @login_szu
    def post(self, request):
        currentUser = get_object_or_404(GiftSystem_user, stu_no=request.session['szu_no'])
        gifts = Gift.objects.filter(own__stu_no=request.session['szu_no'])
        if len(gifts) > 2:
            data = {"status": "full", "message": u"您的礼物数目满了噢"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        given = GivenForm(request.POST)
        gift = GiftForm(request.POST)
        user = UserForm(request.POST)
        if not currentUser.phone or not currentUser.area:
            if user.is_valid():
                phone = user.cleaned_data['phone']
                area = user.data['area']
            else:
                data = {"status": "error","message": user.errors.values()}
                return HttpResponse(json.dumps(data), content_type="application/json")
            currentUser.area = area
            currentUser.phone = phone
            currentUser.save()
        if given.is_valid() and gift.is_valid():
            t = Gift.objects.create(
                name=gift.data["name"],
                type=gift.data["type"],
                description=gift.data["description"],
                isAnonymous=gift.cleaned_data["isAnonymous"],
                giftId=currentUser.area + gift.data["type"] + "{:0>5}".format(
                    len(Gift.objects.filter(own__area=currentUser.area)) + 1)
            )
            try:
                GivenGift.objects.create(
                    givenPerson=given.data["givenPerson"],
                    givenAdress=given.data["givenAdress"],
                    givenPhone=given.cleaned_data["givenPhone"],
                    gift=t
                )
            except:
                t.delete()
            t.own = currentUser
            t.isExchange = False
            t.save()
            data = {'status': 'success', 'message':"您的礼物ID是:%s" % t.giftId}
            return HttpResponse(json.dumps(data), content_type= 'application/json')
        given_message = [i for i in given.errors.values()]
        gift_message = [i for i in gift.errors.values()]
        data = {"status": "error", "message":  given_message + gift_message}
        return HttpResponse(json.dumps(data), content_type="application/json")

#@time_require(starttime="2016-12-8", endtime="2016-12-15")
@login_szu
@readRequire
def giftList(request):
    gifts = Gift.objects.filter(own__stu_no=request.session['szu_no'], isDelete=False)
    gifts_count = 3 - len(gifts)
    return render(request, "christmas/giftList.html", locals())

@login_szu
def index(request):
    try:
        user = GiftSystem_user.objects.get(stu_no = request.session['szu_no'])
    except:
        gender_dict = {
            u'男': 'male',
            u'女': 'female'
        }
        user = GiftSystem_user.objects.create(
               stu_no=request.session['szu_no'],
               name=request.session['szu_name'],
               gender=gender_dict[request.session['szu_sex']]
        )
    return render(request, 'christmas/index.html', locals())

@time_require(starttime="2016-12-12")
@login_szu
def resultList(request):
    mygifts = Gift.objects.filter(own__stu_no=request.session['szu_no'], isDelete=False)
    id_list = []
    for g in mygifts:
        if g.isExchange:
            if g.exchangegift.changeresult.getGiftId:
                id_list.append(g.exchangegift.changeresult.getGiftId)
    gifts = [Gift.objects.get(giftId=gid) for gid in id_list]
    gifts_count = 0
    return render(request, "christmas/giftList.html", locals())

@login_szu
def changeMyInfo(request):
    if request.method == "GET":
        user = GiftSystem_user.objects.get(stu_no=request.session["szu_no"])
        return render(request, "christmas/changeMyInfo.html", locals())
    else:
        user = GiftSystem_user.objects.get(stu_no=request.session["szu_no"])
        userform = UserForm(request.POST, instance=user)
        if userform.is_valid():
            userform.save()
            return HttpResponseRedirect("/christmas/")
        return render(request, "christmas/changeMyInfo.html" ,locals())
 
@login_szu
def postWantType(request):
    if request.method == "POST":
        wantType = request.POST.getlist("wanttype[]")
        giftId = request.POST["giftId"]
        wanttypestring = ''
        for i in wantType:
            wanttypestring = wanttypestring + i + " "
        stu_no = request.session['szu_no']
        gift = Gift.objects.get(giftId=giftId)
        if gift.own.stu_no == stu_no and gift.isExchange:
            try:
                a = gift.exchangegift.changeresult
                data = {"status": "resubmit", "message": "已绑定过想要的礼物类型"}
                return HttpResponse(json.dumps(data), content_type="application/json")
            except:
                if not wanttypestring:
                    data = {"status": "error", "message": "提交的类型为空"}
                    return HttpResponse(json.dumps(data), content_type="application/json")
                print (wanttypestring)
                ChangeResult.objects.create(exchangegift=gift.exchangegift, wangGiftType=wanttypestring)
                data = {"status": "success", "message": "成功添加想要的礼物类型"}
                return HttpResponse(json.dumps(data), content_type="application/json")
    data = {"status": "error", "message": "出了点不知道什么原因的错误呢= =、"}
    return HttpResponse(json.dumps(data), content_type="application/json")

@check_perms('christmas.manager')
def manageIndex(request):
    gift_list = Gift.objects.filter(isDelete=False).order_by('giftId')
    paginator = Paginator(gift_list, 100)
    try:
        page = int(request.GET.get('page', 1))
        gift_list = paginator.page(page)
    except(EmptyPage, InvalidPage):
        gift_list = paginator.page(1)
    return render(request, "christmas/manageIndex.html", locals())

class manageGift(View):
    @method_decorator(check_perms('christmas.manager'))
    def get(self, request):
        gid = request.GET['id']
        gift = get_object_or_404(Gift, pk=gid)
        if gift.isExchange:
            more = ExchangeForm(instance=gift.exchangegift)
        else:
            more = GivenForm(instance=gift.givengift)
        form = GiftForm(instance=gift)
        return render(request, "christmas/form.html", locals())

    @method_decorator(check_perms('christmas.manager'))
    def post(self, request):
        gid = request.GET['id']
        gift = get_object_or_404(Gift, pk=gid)
        form = GiftForm(request.POST, instance=gift)
        form.save()
        if gift.isExchange:
            more = ExchangeForm(request.POST, instance=gift.exchangegift)
        else:
            more = GivenForm(request.POST, instance=gift.givengift)
        more.save()
        return HttpResponseRedirect("/christmas/manage/")

class manageUser(View):
    @method_decorator(check_perms('christmas.manager'))
    def get(self, request):
        uid = request.GET['id']
        user = get_object_or_404(GiftSystem_user, pk=uid)
        user = UserForm(instance=user)
        return render(request, "christmas/user.html", locals())

    @method_decorator(check_perms('christmas.manager'))
    def post(self, request):
        uid = request.GET['id']
        user = get_object_or_404(GiftSystem_user, pk=uid)
        user = UserForm(request.POST, instance=user)
        user.save()
        return HttpResponseRedirect("/christmas/manage/")

# def postWantType(request):
#     if request.method == "POST":
#         wantType = request.POST["wanttype[]"]
#         giftId = request.POST["giftId"]
#         if not wantType or not giftId:
#             data = {"status": "resubmit", "message": "重复提交了"}
#             return HttpResponse(json.dumps(data), content_type="application/json")
#         stu_no = "2015150003"
#         gift = Gift.objects.get(giftId=giftId)
#         if gift.own.stu_no == stu_no and gift.isExchange:
#             thisTypeGifts = Gift.objects.filter(type=wantType, isUsed=False)
#             if thisTypeGifts:
#                 getGift = random.choice(thisTypeGifts)
#                 if gift.exchangegift.changeresult.wangGiftType or gift.exchangegift.changeresult.getGiftId:
#                     data = {"status": "error", "message": "你已经有礼物了"}
#                     return HttpResponse(json.dumps(data), content_type="application/json")
#                 gift.exchangegift.changeresult.wangGiftType = wantType
#                 getId = getGift.giftId
#                 gift.exchangegift.changeresult.getGiftId = getId
#                 gift.exchangegift.changeresult.save()
#                 data = {"status": "success", "message": "获取的礼物ID是" + getId}
#                 return HttpResponse(json.dumps(data), content_type="application/json")
#             data = {"status": "nogift", "message":"没有这种类别的礼物了"}
#             return HttpResponse(json.dumps(data), content_type="application/json")
#     data = {"status": "error", "message": "提交有误"}
#     return HttpResponse(json.dumps(data), content_type="application/json")
