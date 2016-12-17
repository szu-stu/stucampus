#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
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
                year, month, day = endtime.split("-")
            enddate = datetime(int(year), int(month), int(day)).date()
            if now < aimdate:
                return render(request, 'christmas/error.html')
            if endtime:
                if now >= enddate:
                    return render(request, 'christmas/error.html')
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
    @time_require(endtime="2016-12-16")
    @login_szu
    def get(self, request):
        exchange = ExchangeForm()
        gift = GiftForm()
        current_user = GiftSystem_user.objects.get(stu_no=request.session['szu_no'])
        user = UserForm()
        return render(request, 'christmas/addExchange.html', locals())
    
    @time_require(endtime="2016-12-16")
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
    @time_require(endtime="2016-12-16")
    @login_szu
    def get(self, request):
        given = GivenForm()
        gift = GiftForm()
        current_user = GiftSystem_user.objects.get(stu_no=request.session['szu_no'])
        user = UserForm()
        return render(request, "christmas/addGiven.html", locals())
    @time_require(endtime="2016-12-16")
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

@time_require(starttime="2016-12-19")
@login_szu
def resultList(request):
    mygifts = Gift.objects.filter(own__stu_no=request.session['szu_no'], isDelete=False)
    id_list = []
    for g in mygifts:
        if g.isExchange:
            if g.exchangegift.changeresult.getGiftId:
                id_list.append(g.exchangegift.changeresult.getGiftId)
    gifts = [Gift.objects.get(giftId=gid) for gid in id_list]
    gifts_count = len(gifts)
    return render(request, "christmas/resultList.html", locals())

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
    try:
        search = request.GET.get("search")
    except:
        pass
    if search:
        gift_list = Gift.objects.filter(giftId=search).filter(isDelete=False)
        if not gift_list:
            gift_list = Gift.objects.filter(own__name=search).filter(isDelete=False)
    else:
        gift_list = Gift.objects.filter(isDelete=False).order_by('giftId')
    paginator = Paginator(gift_list, 100)
    try:
        page = int(request.GET.get('page', 1))
        gift_list = paginator.page(page)
    except(EmptyPage, InvalidPage):
        gift_list = paginator.page(1)
    return render(request, "christmas/manageIndex.html", locals())

@check_perms('christmas.manager')
def manageGet(request):
    uid = request.POST.get("uid")
    gift = Gift.objects.get(id=uid)
    gift.isGet = True
    gift.save()
    return HttpResponse("")

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

from pyexcelerate import Workbook, Style, Alignment
class makeExcel(View):
    def __init__(self):
#        self.exchange_south_data = [[u'交换礼物登记表--南区'], [u'学号', u'姓名', u'礼物编号', u'礼物类别', u'礼物描述']]
#        self.exchange_wsouth_data = [[u'交换礼物登记表--西南'], [u'学号', u'姓名', u'礼物编号', u'礼物类别', u'礼物描述']]
#        self.exchange_vege_data = [[u'交换礼物登记表--斋区'], [u'学号', u'姓名', u'礼物编号', u'礼物类别', u'礼物描述']]
#        self.given_south_data = [[u'赠与礼物登记表--南区'], [u'学号', u'姓名', u'礼物编号', u'礼物类别', u'礼物描述']]
#        self.given_wsouth_data = [[u'赠与礼物登记表--西南'], [u'学号', u'姓名', u'礼物编号', u'礼物类别', u'礼物描述']]
#        self.given_vege_data = [[u'赠与礼物登记表--斋区'], [u'学号', u'姓名', u'礼物编号', u'礼物类别', u'礼物描述']]
        self.exchange_data = [[u'交换礼物登记表'], [u'学号', u'姓名', u'礼物编号', u'礼物类别', u'礼物描述']]
        self.given_data = [[u'交换礼物登记表'], [u'学号', u'姓名', u'礼物编号', u'礼物类别', u'礼物描述']]
        self.gift_type = {
            "01": u'食物',
            "02": u'服装配饰',
            "03": u'钟表首饰',
            "04": u'化妆品',
            "05": u'运动户外',
            "06": u'电器数码',
            "07": u'小玩意',
            "08": u'手工物件',
            "09": u'二次元',
            "10": u'图书音像',
            "11": u'学习资源',
            "12": u'其他'
        }
#GIFT_TYPE = (
#    ('01', u'食物'),
#    ('02', u'服装配饰'),
#    ('03', u'钟表首饰'),
#    ('04', u'化妆品'),
#    ('05', u'运动户外'),
#    ('06', u'电器数码'),
#    ('07', u'小玩意'),
#    ('08', u'手工物件'),
#    ('09', u'二次元'),
#    ('10', u'图书音像'),
#    ('11', u'学习资源'),
#    ('12', u'其它'),
#)

    @method_decorator(check_perms('christmas.manager'))
    def get(self, request):
        self.make_array()
        self.make_excel()

        def file_iterator(file_name, chunk_size=512):
            with open(file_name, "rb") as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break


        the_file_name = "stucampus/christmas/info/1.xlsx"
        response = StreamingHttpResponse(file_iterator(the_file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
        return response

    def make_array(self):
        '''exchange_south_data_extend = [[i.own.stu_no, i.own.name, i.giftId, self.gift_type[i.type], i.description] for i in
                                      Gift.objects.filter(isDelete=False).filter(own__area="C").filter(isExchange=True)]
        exchange_wsouth_data_extend = [[i.own.stu_no, i.own.name, i.giftId, self.gift_type[i.type], i.description] for i in
                                      Gift.objects.filter(isDelete=False).filter(own__area="A").filter(isExchange=True)]
        exchange_vege_data_extend = [[i.own.stu_no, i.own.name, i.giftId, self.gift_type[i.type], i.description] for i in
                                       Gift.objects.filter(isDelete=False).filter(own__area="B").filter(isExchange=True)]
        given_south_data_extend = [[i.own.stu_no, i.own.name, i.giftId, self.gift_type[i.type], i.description] for i in
                                      Gift.objects.filter(isDelete=False).filter(own__area="C").filter(isExchange=False)]
        given_wsouth_data_extend = [[i.own.stu_no, i.own.name, i.giftId, self.gift_type[i.type], i.description] for i in
                                       Gift.objects.filter(isDelete=False).filter(own__area="A").filter(isExchange=False)]
        given_vege_data_extend = [[i.own.stu_no, i.own.name, i.giftId, self.gift_type[i.type], i.description] for i in
                                     Gift.objects.filter(isDelete=False).filter(own__area="B").filter(isExchange=False)]
        self.exchange_south_data = self.exchange_south_data + exchange_south_data_extend
        self.exchange_wsouth_data = self.exchange_wsouth_data + exchange_wsouth_data_extend
        self.exchange_vege_data = self.exchange_vege_data + exchange_vege_data_extend
        self.given_south_data = self.given_south_data + given_south_data_extend
        self.given_wsouth_data = self.given_wsouth_data + given_wsouth_data_extend
        self.given_vege_data = self.given_vege_data + given_vege_data_extend'''
        exchange_data_extend = [[i.own.stu_no, i.own.name, i.giftId, self.gift_type[i.type], i.description] for i in
                                        Gift.objects.filter(isDelete=False).filter(isExchange=True)]
        given_data_extend = [[i.own.stu_no, i.own.name, i.giftId, self.gift_type[i.type], i.description] for i in
                                        Gift.objects.filter(isDelete=False).filter(isExchange=False)]
        self.exchange_data = self.exchange_data + exchange_data_extend
        self.given_data = self.given_data + given_data_extend

    def make_excel(self):
        def set_style(the_ws):
            ws_style = Style(size=15, alignment=Alignment(horizontal="center", vertical="center"))
            the_ws.range("A1", "E1").merge()
            for i in range(1, 5):
                the_ws.set_col_style(i, ws_style)
            the_ws.set_col_style(5, Style(size=30, alignment=Alignment(horizontal="center", vertical="center")))

        wb = Workbook()
       # ws = wb.new_sheet(u"南区交换", data=self.exchange_south_data)
       # set_style(ws)
       # ws = wb.new_sheet(u"西南交换", data=self.exchange_wsouth_data)
       # set_style(ws)
       # ws = wb.new_sheet(u"斋区交换", data=self.exchange_vege_data)
       # set_style(ws)
       # ws = wb.new_sheet(u"南区赠与", data=self.given_south_data)
       # set_style(ws)
       # ws = wb.new_sheet(u"西南赠与", data=self.given_wsouth_data)
       # set_style(ws)
       # ws = wb.new_sheet(u"斋区赠与", data=self.given_vege_data)
       # set_style(ws)
        ws = wb.new_sheet(u'交换表', data=self.exchange_data)
        set_style(ws)
        ws = wb.new_sheet(u'赠与表', data=self.given_data)
        set_style(ws)
        wb.save('stucampus/christmas/info/1.xlsx')

class makeResultExcel(View):
    def __init__(self):
        self.exchange_data = [[u'礼物交换表'], [u'姓名', u'性别', u'礼物名字', u'礼物编号', u'获得礼物名字', u'礼物ID']]

    @method_decorator(check_perms('christmas.manager'))
    def get(self, request):
        self.make_array()
        self.make_excel()

        def file_iterator(file_name, chunk_size=512):
            with open(file_name, "rb") as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        the_file_name = "stucampus/christmas/info/2.xlsx"
        response = StreamingHttpResponse(file_iterator(the_file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
        return response

    def make_array(self):
        exchange_data_extend = [[i.own.name, i.own.gender , i.name, i.giftId, Gift.objects.get(giftId=i.exchangegift.changeresult.getGiftId).name, i.exchangegift.changeresult.getGiftId] for i in
                                        Gift.objects.filter(isDelete=False).filter(isExchange=True).filter(isGet=True)]
        self.exchange_data = self.exchange_data + exchange_data_extend

    def make_excel(self):
        wb = Workbook()
        ws = wb.new_sheet(u'交换表', data=self.exchange_data)
        wb.save('stucampus/christmas/info/2.xlsx')

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
