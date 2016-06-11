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
import time,random
from itertools import chain


# Create your views here.

class AddPlan(View):

    @login_szu
    def get(self,request,category_english_name=None):
        '''
            假登陆
        '''
        return HttpResponseRedirect(reverse('summer_plans:list',args=(category_english_name,)))

    @login_szu
    def post(self,request,category_english_name=None):
        form = PlanForm(request.POST)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='errors', messages=messages)
        if User.objects.filter(szu_no=request.session['szu_no'],email=None).exclude().exists():
            #用户存在,但是没有email
            if not form.cleaned_data['email']:
                return spec_json(status='errors', messages=u"email必填")
            author = get_object_or_404(User,szu_no=request.session['szu_no'])
            author.email = form.cleaned_data['email']
            author.save()
        elif User.objects.filter(szu_no=request.session['szu_no']).exclude(email=None).exists():
            #用户存在,有email
            author = get_object_or_404(User,szu_no=request.session['szu_no'])
            author.email = form.cleaned_data['email'] if form.cleaned_data['email'] else author.email
            author.save()
        else:
            #用户不存在
            if not form.cleaned_data['email']:
                return spec_json(status='errors', messages=u"email必填")
            author = User(szu_no=request.session['szu_no'],
                        szu_name=request.session['szu_name'],
                        szu_ic=request.session['szu_ic'],
                        szu_org_name=request.session['szu_org_name'].split("/")[1],
                        szu_sex=request.session['szu_sex'],
                        email=form.cleaned_data['email'],
                        avatar_color=random.randint(1,5),
                        )
            author.save()
        plan_category = get_object_or_404(PlanCategory,english_name=category_english_name)
        plan = form.save(commit=False)
        plan.category = plan_category
        plan.author = author
        plan.save()
        return render_json({"status":"success","redirect_url":reverse('summer_plans:list',args=(category_english_name,))})

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
    plan_list = Plan.objects.filter(
                                    Q(content__icontains=q)|   #查找内容 
                                    Q(author__szu_name__icontains=q,is_anon=False)|#查找真实姓名
                                    Q(alias__icontains=q,is_anon=True)|#查找匿名
                                    Q(author__szu_org_name__icontains=q),#查找学院
                                    category=plan_category,
                                ).distinct().order_by("-pk")#去重，按照时间先后排序
    return return_plan_list(request,plan_list,plan_category,title=u"【搜索结果】")

def has_thought_plan_list(request,category_english_name):
    '''
        发表过感想的列表
    '''
    plan_category = get_object_or_404(PlanCategory,english_name=category_english_name,is_on=True)
    plan_list = Plan.objects.filter(category=plan_category).exclude(thought=None).order_by("-like_count")
    return return_plan_list(request,plan_list,plan_category,title=u"【计划感想】")

def plan_list(request, category_english_name=None):
    '''
        首页显示
    '''
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
    return return_plan_list(request,plan_list,plan_category,title=u"【点赞排行】")

def self_plan(request,category_english_name,szu_no):
    plan_category = get_object_or_404(PlanCategory, english_name=category_english_name,is_on=True)
    author = get_object_or_404(User,szu_no=szu_no)
    plan_list = Plan.objects.filter(category=plan_category,author=author,deleted=False).order_by('-pk')
    return return_plan_list(request,plan_list,plan_category,title=u"【我的计划】")

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
    '''
        发表感想
    '''
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
    if not request.session.get("szu_no"):
        return None
    if User.objects.filter(szu_no=request.session['szu_no']).exists():#email
        author = get_object_or_404(User,szu_no=request.session['szu_no'])
    else:
        author = User(szu_no=request.session['szu_no'],
                        szu_name=request.session['szu_name'],
                        szu_ic=request.session['szu_ic'],
                        szu_org_name=request.session['szu_org_name'].split("/")[1],
                        szu_sex=request.session['szu_sex'],
                        avatar_color=random.randint(1,5),
                        )
        author.save()
    return author


def return_plan_list(request,plan_list,plan_category,title=""):
    '''
        工具函数 根据传来的list返回
    '''
    paginator = Paginator(plan_list, 5)
    try:
        plan_list = paginator.page(request.GET.get('page'))
    except InvalidPage:
        plan_list = paginator.page(1)
    if not request.is_ajax():
        user = get_user(request)
        return render(request, "summer_plans/index.html",{'plan_list':plan_list,'plan_category':plan_category,'user':user,'title':title})
    else:
        return render(request, "summer_plans/ajax_plan_list.html",{'plan_list':plan_list,'plan_category':plan_category})