#-*- coding: UTF-8 -*-   

from django.shortcuts import render
from django.core.paginator import InvalidPage,Paginator
from django.http import *
from django.core.urlresolvers import reverse
from django.views.generic import View

from stucampus.dreamer.models import Register
from stucampus.dreamer.forms import Register_Form
from stucampus.account.permission import check_perms

from django.db.models import Q
import datetime
def signup_mobile(request):
     return render(request, 'dreamer/apply_mobile.html', {'form': Register_Form()})

class SignUp(View):
    def get(self, request):
        if request.META['HTTP_USER_AGENT'].lower().find('mobile') > 0:
            return HttpResponseRedirect('/dreamer/mobile/')
        else:
            return render(request, 'dreamer/apply.html', {'form': Register_Form()})
    def post(self, request):
        msg = Register()
        tmp = Register_Form(request.POST)
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
            msg.ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            msg.ip = request.META['REMOTE_ADDR'] 
        msg.status = True
        now = datetime.date.today()
        if tmp.is_valid():
            msg.name = tmp.cleaned_data['name']
            msg.gender = tmp.cleaned_data['gender']
            msg.stu_ID = tmp.cleaned_data['stu_ID']
            msg.college = tmp.cleaned_data['college']
            msg.mobile = tmp.cleaned_data['mobile']
            msg.dept1 = tmp.cleaned_data['dept1']
            msg.dept2 = tmp.cleaned_data['dept2']
            msg.self_intro = tmp.cleaned_data['self_intro']
            same_SID = Register.objects.filter(stu_ID = msg.stu_ID, status=True).count()
            if same_SID > 0:
                print "1"
                return render(request, 'dreamer/failed.html')
            else:
                if Register.objects.filter(sign_up_date=now).filter(ip=msg.ip).count()>=50:  
                    tip="您当前IP已于同一天成功报名五十次，请等候第二天或换另一台电脑再进行报名"	
                    return render(request, 'dreamer/failed.html',{'tip':tip})
                else:
                    msg.save()
                    return render(request, 'dreamer/succeed.html', {'form': msg})
        else:
            return render(request, 'dreamer/failed.html')


def index(request):
    if request.method == 'GET':
        return render(request, 'dreamer/index.html')


class CheckMsg(View):

    def get(self, request):
        return render(request, 'dreamer/check_msg.html')

    def post(self, request):
        search=req.POST['search']
        objects = Register.objects.filter(Q(name=search)|Q(stu_ID=search)&Q(status=True)).count()
        if objects>0:
            return HttpResponse("已报名成功")
        else:
            return HttpResponse("尚未进行报名或报名不成功，若有疑问请在群里反映.")


def succeed(request):
    return render(request, 'dreamer/succeed.html')

def check(request):
    aaa = Register.objects.all().count()
    return HttpResponse(aaa)

@check_perms('dreamer.manager')
def alldetail(request):
    aall = Register.objects.filter(status=True)
    user = request.user

    cbb1 = aall.filter(dept1="cbb")
    cbb2 = aall.filter(dept2="cbb")
    cbbb = cbb1.filter(gender="boy").count()+cbb2.filter(gender="boy").count()
    cbbg = cbb1.filter(gender="girl").count()+cbb2.filter(gender="girl").count()

    jsb1 = aall.filter(dept1="jsb")
    jsb2 = aall.filter(dept2="jsb")
    jsbb = jsb1.filter(gender="boy").count()+jsb2.filter(gender="boy").count()
    jsbg = jsb1.filter(gender="girl").count()+jsb2.filter(gender="girl").count()

    sjb1 = aall.filter(dept1="sjb")
    sjb2 = aall.filter(dept2="sjb")
    sjbb = sjb1.filter(gender="boy").count()+sjb2.filter(gender="boy").count()
    sjbg = sjb2.filter(gender="girl").count()+sjb1.filter(gender="girl").count()

    xzb1 = aall.filter(dept1="xzb")
    xzb2 = aall.filter(dept2="xzb")
    xzbb = xzb1.filter(gender="boy").count()+xzb2.filter(gender="boy").count()
    xzbg = xzb1.filter(gender="girl").count()+xzb2.filter(gender="girl").count()

    yyb1 = aall.filter(dept1="yyb")
    yyb2 = aall.filter(dept2="yyb")
    yybb = yyb1.filter(gender="boy").count()+yyb2.filter(gender="boy").count()
    yybg = yyb1.filter(gender="girl").count()+yyb2.filter(gender="girl").count()

    return render(request,'dreamer/situation.html',{"jsb1":jsb1.count(),"jsb2":jsb2.count(),"jsbb":jsbb,"jsbg":jsbg,
                                                    "sjb1":sjb1.count(),"sjb2":sjb2.count(),"sjbb":sjbb,"sjbg":sjbg,
                                                    "xzb1":xzb1.count(),"xzb2":xzb2.count(),"xzbb":xzbb,"xzbg":xzbg,
                                                    "yyb1":yyb1.count(),"yyb2":yyb2.count(),"yybb":yybb,"yybg":yybg,
                                                    "cbb1":cbb1.count(),"cbb2":cbb2.count(),"cbbb":cbbb,"cbbg":cbbg,
                                                    "all" :aall.count(),"user":user})

@check_perms('dreamer.manager')
def alllist(request):
    applyall = Register.objects.filter(status=True).order_by('sign_up_date')
    paginator = Paginator(applyall,8)
    page = request.GET.get('page')
    try:
        page = paginator.page(page)
    except InvalidPage:
        page = paginator.page(1)
    return render(request,'dreamer/list.html',{'page':page})

@check_perms('dreamer.manager')
def delete(request):
    apply_id = request.GET.get('id')
    app = Register.objects.get(id=apply_id)
    app.status = False
    app.save()
    return HttpResponseRedirect('/dreamer/manage/')

@check_perms('dreamer.manager')
def search(request):
    search=request.GET.get('search')
    app = Register.objects.filter(status=True).filter(Q(name=search)|Q(stu_ID=search))
    paginator = Paginator(app,8)
    page = request.GET.get('page')
    try:
        page = paginator.page(page)
    except InvalidPage:
        page = paginator.page(1)
    return render(request,'dreamer/list.html',{'page':page})

@check_perms('dreamer.manager')
def detail(request):
    apply_id = request.GET.get('id')
    app = Register.objects.get(id=apply_id)
    print app.name
    return render(request,'dreamer/detail.html',{'app':app})
