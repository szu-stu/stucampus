#-*- coding: utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404,HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.core.paginator import InvalidPage, Paginator
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.mail import send_mail,send_mass_mail,EmailMultiAlternatives

from .forms import PlanForm,PlanThoughtForm
from .models import Plan,PlanCategory,User
from stucampus.utils import spec_json,render_json
from stucampus.account.permission import check_perms

from login_szu import login_szu
import datetime
import time
from itertools import chain


# Create your views here.

class AddPlan(View):

    @login_szu
    def get(self,request,category_english_name=None):
        return HttpResponseRedirect(reverse('summer_plans:list',args=(category_english_name,)))

    @login_szu
    def post(self,request,category_english_name=None):
        form = PlanForm(request.POST)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='errors', messages=messages)
        if User.objects.filter(szu_no=request.session['szu_no']).exclude(email=None).exists():#要考虑先点赞，后发表的情况
            author = get_object_or_404(User,szu_no=request.session['szu_no'])
        elif User.objects.filter(szu_no=request.session['szu_no'],email=None).exists():
            author = get_object_or_404(User,szu_no=request.session['szu_no'])
            author.email = form.cleaned_data['email']
            author.save()
        else:
            author = User(szu_no=request.session['szu_no'],
                        szu_name=request.session['szu_name'],
                        szu_ic=request.session['szu_ic'],
                        szu_org_name=request.session['szu_org_name'].split("/")[1],
                        szu_sex=request.session['szu_sex'],
                        email=form.cleaned_data['email']
                        )
            author.save()
        plan_category = get_object_or_404(PlanCategory,english_name=category_english_name)
        plan = form.save(commit=False)
        plan.category = plan_category
        plan.author = author
        plan.save()
        return spec_json(status='success')

@login_szu
def like(request,category_english_name=None):
    '''
        点赞
    '''
    plan_id = request.GET.get('plan_id')
    if not plan_id:
        messages=u"传入参数有误"
        return spec_json(status='errors',messages=messages)
    plan = get_object_or_404(Plan,pk=plan_id)
    author = get_user(request) #获取当前的用户
    if author not in plan.like_persons.all():
        plan.like_persons.add(author)
        plan.like_count = len(plan.like_persons.all())
    else:
        plan.like_persons.remove(author)
        plan.like_count = len(plan.like_persons.all())
    plan.save()
    like_persons = plan.like_persons.all()
    like_persons_list=[ {"szu_name":person.szu_name,"szu_no":person.szu_no} for person in like_persons]
    return render_json({'status':'success','like_persons':like_persons_list})

def search(request,category_english_name=None):
    q = request.GET.get('q')
    if not q:
        return HttpResponseRedirect(reverse('summer_plans:list',args=(category_english_name,)))
    plan_category = get_object_or_404(PlanCategory,english_name=category_english_name,is_on=True)
    plan1 = Plan.objects.filter(Q(category=plan_category)&Q(content__icontains=q))
    author_list = User.objects.filter(Q(szu_name__icontains=q)|Q(szu_org_name__icontains=q))
    plan_list=[]
    plan_list.extend(plan1)
    for author in author_list:          #将包含的作者的plan合并进来
        plan2 = Plan.objects.filter(Q(category=plan_category)&Q(author_id=author.pk))
        plan_list.extend(plan2)
    plan_list = set(plan_list)#去重
    plan_list =list(plan_list)
    return return_plan_list(request,plan_list,plan_category)

def plan_list(request, category_english_name=None):
    plan_category = get_object_or_404(PlanCategory, english_name=category_english_name,is_on=True)
    plan_list = Plan.objects.filter(category=plan_category,
                                          deleted=False).order_by('-pk')
    return return_plan_list(request,plan_list,plan_category)

def like_ranking_list(request, category_english_name=None):
    '''
        根据点赞数排序
    '''
    plan_category = get_object_or_404(PlanCategory, english_name=category_english_name,is_on=True)
    plan_list = Plan.objects.filter(category=plan_category,
                                          deleted=False).order_by('-like_count')
    return return_plan_list(request,plan_list,plan_category)

def self_plan(request,category_english_name,szu_no):
    plan_category = get_object_or_404(PlanCategory, english_name=category_english_name,is_on=True)
    author = get_object_or_404(User,szu_no=szu_no)
    plan_list = Plan.objects.filter(category=plan_category,author=author,deleted=False).order_by('-pk')
    return return_plan_list(request,plan_list,plan_category)

@login_szu
def logout(request,category_english_name):
    del request.session['szu_no'],
    del request.session['szu_name'],
    del request.session['szu_ic'],
    del request.session['szu_org_name']
    del request.session['szu_sex']
    return HttpResponseRedirect(reverse('summer_plans:list',args=(category_english_name,)))

@login_szu
def delete(request,category_english_name,id):
    author = get_user(request)
    plan = get_object_or_404(Plan, author=author,pk=id)
    plan.deleted = True
    plan.save()
    return HttpResponseRedirect(reverse('summer_plans:list',args=(category_english_name,)))

@login_szu
def post_thought(request,category_english_name,id):
    plan_category = get_object_or_404(PlanCategory, english_name=category_english_name,is_on=True)
    if not plan_category.tip_time:
        messages=u"没有设置提醒时间"
        return spec_json(status='errors', messages=messages) 
    time_interval = datetime.date.today() - plan_category.tip_time
    if time_interval.total_seconds()<0:
        messages=u"还没到指定时间，不能发表感想"
        return spec_json(status='errors', messages=messages)
    author = get_user(request)
    plan = get_object_or_404(Plan, author=author,pk=id)
    form = PlanThoughtForm(request.POST,instance=plan)
    if not form.is_valid():
        messages = form.errors.values()
        return spec_json(status='errors', messages=messages)
    form.save()
    return spec_json(status='success')

@check_perms('summer_plans.send_email')
def senf_email_to_plan_author(request,category_english_name=None):
    '''  
        发送邮件给用户
    '''
    plan_category = get_object_or_404(PlanCategory,english_name=category_english_name)
    time_interval = datetime.date.today() - plan_category.tip_time
    if time_interval.total_seconds()<0:
        return  HttpResponse(u"感悟留言时间还未到，邮件不能发送")
    
    plan_list = plan_category.plan_set.all()
    email_set = set()
    for plan in plan_list:
        if plan.author.email:
            email_set.add(str(plan.author.email))
    subject = u"深圳大学【学子天地】"+plan_category.name
    message = u"放假回来了，还记得你在<a href='http://stu.szu.edu.cn%s'>%s</a>写下的计划吗？快来回复你的感悟吧.回复感悟将有机会参与抽奖哦!!快点行动吧"%(reverse('summer_plans:list',args=(category_english_name,)),subject)
    email_list = list(email_set)
    try:
        send_mail(subject=subject, message=message, from_email=None,recipient_list=email_list, fail_silently=False,html_message=message) 
    except Exception, e:
        send_mail(subject="error", message="发送邮件出错", from_email=None,recipient_list=['jimczj@qq.com'], fail_silently=False)
    finally:
        return  HttpResponse(u"已经成功发送邮件")

    



def get_user(request):
    '''
        工具函数 返回用户
    '''
    if User.objects.filter(szu_no=request.session['szu_no']).exists():#email
        author = get_object_or_404(User,szu_no=request.session['szu_no'])
    else:
        author = User(szu_no=request.session['szu_no'],
                        szu_name=request.session['szu_name'],
                        szu_ic=request.session['szu_ic'],
                        szu_org_name=request.session['szu_org_name'].split("/")[1],
                        szu_sex=request.session['szu_sex']
                        )
        author.save()
    return author


def return_plan_list(request,plan_list,plan_category):
    '''
        工具函数 根据传来的list返回
    '''
    paginator = Paginator(plan_list, 5)
    try:
        plan_list = paginator.page(request.GET.get('page'))
    except InvalidPage:
        plan_list = paginator.page(1)
    if not request.is_ajax():
        return render(request, "summer_plans/index.html",{'plan_list':plan_list,'plan_category':plan_category})
    else:
        return render(request, "summer_plans/ajax_plan_list.html",{'plan_list':plan_list,'plan_category':plan_category})