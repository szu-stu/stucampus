#-*- coding: utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.core.paginator import InvalidPage, Paginator
from django.utils.decorators import method_decorator

from .forms import PlanForm
from .models import Plan,PlanCategory,User
from stucampus.utils import spec_json,render_json

from login_szu import login_szu
import time


# Create your views here.

def index(request):
    if not request.is_ajax():
    	form = PlanForm()
        plan_list = Plan.objects.filter(
                        deleted=False).order_by("-pk")[:7]  
        paginator = Paginator(plan_list, 6)
        plan_list = paginator.page(1)
        plan = plan_list[0]
        return render(request, "summer_plans/index.html",{'plan_list': plan_list,'form':form})
    else:
        plan_list = Plan.objects.filter(deleted=False).order_by('-pk')
        paginator = Paginator(plan_list, 5)
        try:
            plan_list = paginator.page(request.GET.get('page'))
        except InvalidPage:
            plan_list = paginator.page(1)      
        return render(request, "summer_plans/ajax_plan_list.html",{'plan_list':plan_list})


class AddPlan(View):

    @login_szu
    def get(self,request):
        return HttpResponseRedirect(reverse('summer_plans:index'))

    @login_szu
    def post(self,request):
        form = PlanForm(request.POST)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='errors', messages=messages)
        if User.objects.filter(szu_no=request.session['szu_no']).exists():#email
            author = get_object_or_404(User,szu_no=request.session['szu_no'])
        else:
            author = User(szu_no=request.session['szu_no'],
                        szu_name=request.session['szu_name'],
                        szu_ic=request.session['szu_ic'],
                        szu_org_name=request.session['szu_org_name'],
                        szu_sex=request.session['szu_sex'],
                        email=form.cleaned_data['email']
                        )
            author.save()
        plan_category = get_object_or_404(PlanCategory,pk=1)
        plan = form.save(commit=False)
        plan.category = plan_category
        plan.author = author
        plan.save()
        return spec_json(status='success')

def like(request):
    '''
        点赞
    '''
    plan_id = request.GET.get('plan_id')
    if not plan_id:
        messages=u"传入参数有误"
        return spec_json(status='errors',messages=messages)
    plan = get_object_or_404(Plan,pk=plan_id)
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
    if author not in plan.like_persons.all():
        plan.like_persons.add(author)
    else:
        plan.like_persons.remove(author)
    plan.save()
    like_persons = plan.like_persons.all()
    like_persons_list=[ {"szu_name":person.szu_name} for person in like_persons]
    return render_json({'status':'success','like_persons':like_persons_list})


