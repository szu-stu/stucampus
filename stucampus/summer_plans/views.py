#-*- coding: utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404,HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.core.paginator import InvalidPage, Paginator
from django.utils.decorators import method_decorator
from django.db.models import Q

from .forms import PlanForm
from .models import Plan,PlanCategory,User
from stucampus.utils import spec_json,render_json

from login_szu import login_szu
import time
from itertools import chain


# Create your views here.

class AddPlan(View):

    @login_szu
    def get(self,request,category_english_name=None):
        plan_category = get_object_or_404(PlanCategory,english_name=category_english_name)
        return HttpResponseRedirect(reverse('summer_plans:list',args=(plan_category.english_name,)))

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
                        szu_org_name=request.session['szu_org_name'],
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
    else:
        plan.like_persons.remove(author)
    plan.save()
    like_persons = plan.like_persons.all()
    like_persons_list=[ {"szu_name":person.szu_name,"szu_no":person.szu_name} for person in like_persons]
    return render_json({'status':'success','like_persons':like_persons_list})

def search(request,category_english_name=None):
    q = request.GET.get('q')
    plan_category = get_object_or_404(PlanCategory,english_name=category_english_name,is_on=True)
    plan_list = Plan.objects.filter(Q(category=plan_category)&Q(content__icontains=q))
    author_list = User.objects.filter(Q(szu_name__icontains=q)|Q(szu_org_name__icontains=q))
    for author in author_list:          #将包含的作者的plan合并进来
        plans = Plan.objects.filter(Q(category=plan_category)&Q(author_id=author.pk))
        plan_list = chain(plan_list,plans)
    return return_plan_list(request,plan_list,plan_category)

def plan_list(request, category_english_name=None):
    plan_category = get_object_or_404(PlanCategory, english_name=category_english_name,is_on=True)
    plan_list = Plan.objects.filter(category=plan_category,
                                          deleted=False).order_by('-pk')
    return return_plan_list(request,plan_list,plan_category)

@login_szu
def self_plan(request,category_english_name):
    author = get_user(request)
    plan_category = get_object_or_404(PlanCategory, english_name=category_english_name,is_on=True)
    plan_list = Plan.objects.filter(category=plan_category,author=author,deleted=False).order_by('-pk')
    return return_plan_list(request,plan_list,plan_category)


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
                        szu_org_name=request.session['szu_org_name'],
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
        return render(request, "summer_plans/ajax_plan_list.html",{'plan_list':plan_list})