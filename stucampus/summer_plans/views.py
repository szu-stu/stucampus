#-*- coding: utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404,HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.core.paginator import InvalidPage, Paginator
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.mail import send_mail,send_mass_mail,EmailMultiAlternatives

from .forms import PlanForm,PlanThoughtForm,PlanRecordForm
from .models import Plan,PlanCategory,User,PlanRecord,Lottery,LotteryList
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
                        szu_org_name=request.session['szu_org_name'],
                        szu_sex=request.session['szu_sex'],
                        email=form.cleaned_data['email'],
                        avatar_color=get_avator_color(request),
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
    plan_list = Plan.objects.filter(category=plan_category,deleted=False).exclude(thought=None).order_by("-like_count")
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
    return render_json({"status":"success","redirect_url":reverse('summer_plans:list',args=(category_english_name,))})

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

@login_szu
def add_plan_record(request,category_english_name,id):
    #此id是关联的plan的id
    plan_category = get_object_or_404(PlanCategory,english_name=category_english_name)
    plan = get_object_or_404(Plan,category=plan_category,pk=id)
    form = PlanRecordForm(request.POST)
    if plan.author.szu_no != request.session.get("szu_no"):
        messages = u"你没有权限"
        return spec_json(status='errors', messages=messages)
    if not form.is_valid():
        messages = form.errors.values()
        return spec_json(status='errors', messages=messages)
    plan_record = form.save(commit=False)
    plan_record.plan = plan
    plan_record.save()
    return render_json({"status":"success","redirect_url":reverse('summer_plans:list',args=(category_english_name,))})

@login_szu
def delete_plan_record(request,category_english_name,id):
    plan_record = get_object_or_404(PlanRecord,pk=id)
    if plan_record.plan.author.szu_no != request.session.get("szu_no"):
        messages = u"你没有权限"
        return spec_json(status='errors', messages=messages)
    plan_record.delete()
    return render_json({"status":"success","redirect_url":reverse('summer_plans:list',args=(category_english_name,))})

@login_szu
def update_plan_record(request,category_english_name,id):
    plan_record = get_object_or_404(PlanRecord,pk=id)
    if plan_record.plan.author.szu_no != request.session.get("szu_no"):
        messages = u"你没有权限"
        return spec_json(status='errors', messages=messages)
    form = PlanRecordForm(request.POST,instance=plan_record)
    if not form.is_valid():
        messages = form.errors.values()
        return spec_json(status='errors', messages=messages)
    form.save()
    return render_json({"status":"success","redirect_url":reverse('summer_plans:list',args=(category_english_name,))})

@login_szu
def draw(request,category_english_name,id):
    '''
        用户抽奖,该id为抽奖名单id
    '''

    lottery_list = get_object_or_404(LotteryList,pk=id,is_on=True)
    start_time_interval = datetime.date.today() - lottery_list.start_date
    end_time_interval = datetime.date.today()-lottery_list.end_date
    if start_time_interval.total_seconds()<0:
        messages=u"还没到抽奖时间哦，敬请期待"
        return spec_json(status='errors', messages=messages)
    if end_time_interval.total_seconds()>0:
        messages=u"抽奖已经结束，感谢你的参与"
        return spec_json(status='errors', messages=messages)
    user =get_user(request)
    if  lottery_list.lottery.count() == 0:
        messages = u"对不起，没有抽奖名单"
        return spec_json(status='errors', messages=messages)
    lottery_list_person = [lottery.person for lottery in lottery_list.lottery.all()]
    if user not in lottery_list_person:
        messages = u"对不起，你没有资格抽奖"
        return spec_json(status='errors', messages=messages)
    lotterys = lottery_list.lottery.filter(person=user,result=0)
    if not lotterys.exists():
        messages = u"对不起，你已经抽过奖了"
        return spec_json(status='errors', messages=messages)
    lottery = lotterys[0]
    lottery.result = random.randint(1,10000000)
    lottery.save()
    return render_json({"status":"success","lottery_result":lottery.result,"redirect_url":reverse('summer_plans:list',args=(category_english_name,))})

def show_lottery_list(request,category_english_name,id):
    '''
        用户抽奖,该id为抽奖名单id
    '''
    lottery_list = get_object_or_404(LotteryList,pk=id,is_on=True)
    plan_category = get_object_or_404(PlanCategory,english_name=category_english_name)
    title = "【%s】"%lottery_list.name
    rank = get_rank(request,lottery_list)
    return render(request, "summer_plans/lottery_list.html",{'lottery_list':lottery_list,'plan_category':plan_category,'title':title,"rank":rank})




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
                        szu_org_name=request.session['szu_org_name'],
                        szu_sex=request.session['szu_sex'],
                        avatar_color=get_avator_color(request),
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

def get_rank(request,lottery_list):
    '''
        工具函数，获取排名
    '''
    user = get_user(request)
    if user is None:
        return None
    sorted_lotterys = lottery_list.lottery.all().order_by("-result")
    for i in range(len(sorted_lotterys)):
        if user == sorted_lotterys[i].person:
            return i+1
    return None

def get_avator_color(request):
    if request.session.get("szu_sex") == u"男":
        return random.randint(1,2)
    return random.randint(3,5)
