#-*- coding: UTF-8 -*-   

from django.shortcuts import render
from django.core.paginator import InvalidPage,Paginator
from django.http import *
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.db.models import Q

from stucampus.dreamer.models import Register
from stucampus.dreamer.forms import Register_Form
from stucampus.account.permission import check_perms
from stucampus.utils import spec_json,render_json

import datetime
from login_szu import login_szu



class SignUp(View):
    def get(self, request):
        if request.session.get('szu_no') is None:
            is_login=False
            return render(request, 'dreamer/index.html', {'is_login': is_login})
        else:
            is_login=True
            is_registered=False
            if Register.objects.filter(stu_ID=request.session['szu_no']).exists():
                szu_name=request.session['szu_name']
                is_registered=True
                return render(request, 'dreamer/index.html', {'is_login': 				is_login,'is_registered':is_registered,'szu_name':szu_name})
            return render(request, 'dreamer/index.html', {'is_login': is_login,'is_registered':is_registered,'Register_Form':Register_Form()})

    @login_szu
    def post(self, request):
        if Register.objects.filter(stu_ID=request.session['szu_no']).exists():
            messages = u"您已经成功报名过，不能重复报名，如需更改信息，请联系学子天地工作人员"
            return spec_json(status='errors', messages=messages)
        form = Register_Form(request.POST)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='errors', messages=messages)
        register = form.save(commit=False)
        register.name=request.session['szu_name']
        register.gender=request.session['szu_sex']
        register.college=request.session['szu_org_name']
        register.stu_ID=request.session['szu_no']
        register.grade=request.session['szu_no'][:4]
        register.save()
        return render_json({"status":"success","name":register.name})
		

@login_szu
def login_redirect(request):
    return HttpResponseRedirect(reverse('dreamer:joinus')+"#page4")





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
    cbbb = cbb1.filter(gender="male").count()+cbb2.filter(gender="male").count()
    cbbg = cbb1.filter(gender="female").count()+cbb2.filter(gender="female").count()

    jsb1 = aall.filter(dept1="jsb")
    jsb2 = aall.filter(dept2="jsb")
    jsbb = jsb1.filter(gender="male").count()+jsb2.filter(gender="male").count()
    jsbg = jsb1.filter(gender="female").count()+jsb2.filter(gender="female").count()

    sjb1 = aall.filter(dept1="sjb")
    sjb2 = aall.filter(dept2="sjb")
    sjbb = sjb1.filter(gender="male").count()+sjb2.filter(gender="male").count()
    sjbg = sjb2.filter(gender="female").count()+sjb1.filter(gender="female").count()

    xzb1 = aall.filter(dept1="xzb")
    xzb2 = aall.filter(dept2="xzb")
    xzbb = xzb1.filter(gender="male").count()+xzb2.filter(gender="male").count()
    xzbg = xzb1.filter(gender="female").count()+xzb2.filter(gender="female").count()

    yyb1 = aall.filter(dept1="yyb")
    yyb2 = aall.filter(dept2="yyb")
    yybb = yyb1.filter(gender="male").count()+yyb2.filter(gender="male").count()
    yybg = yyb1.filter(gender="female").count()+yyb2.filter(gender="female").count()

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
    app = Register.objects.filter(status=True).filter(name__contains=search)
    if not app:
        if search.isdigit()==True:
            app = Register.objects.filter(status=True).filter(stu_ID=search)
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
    return render(request,'dreamer/detail.html',{'app':app})

@check_perms('dreamer.manager')
def modify(request):
    apply_id = request.POST['id']
    a = Register.objects.get(id=apply_id)
    a.name = request.POST['name']
    gender = request.POST['sex']
    if gender==u'男':
        a.gender = 'male'
    elif gender==u'女':
        a.gender = 'female'
    a.stu_ID = request.POST['stu_id']
    a.college = request.POST['college']
    a.mobile = request.POST['mobile']
    if request.POST['desired_dept_1']==u'行政部':
        a.dept1 = 'xzb'
    if request.POST['desired_dept_1']==u'设计部':
        a.dept1 = 'sjb'
    if request.POST['desired_dept_1']==u'技术部':
        a.dept1 = 'jsb'
    if request.POST['desired_dept_1']==u'采编部':
        a.dept1 = 'cbb'
    if request.POST['desired_dept_1']==u'运营部':
        a.dept1 = 'yyb'
    if request.POST['desired_dept_2']==u'行政部':
        a.dept2 = 'xzb'
    if request.POST['desired_dept_2']==u'设计部':
        a.dept2 = 'sjb'
    if request.POST['desired_dept_2']==u'技术部':
        a.dept2 = 'jsb'
    if request.POST['desired_dept_2']==u'采编部':
        a.dept2 = 'cbb'
    if request.POST['desired_dept_2']==u'运营部':
        a.dept2 = 'yyb'
    a.self_intro = request.POST['introduce']
    a.save()
    return HttpResponseRedirect('/dreamer/manage/detail/?id='+apply_id)
