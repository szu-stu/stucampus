#-*- coding: utf-8
import re
import requests
from lxml import etree

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import View

from stucampus.minivideo.models import Resource, Vote
from stucampus.minivideo.forms import SignUpForm, CommitForm, loginForm
from stucampus.account.permission import check_perms


class SignUpView(View):
    def get(self, request):
        resource_id = request.GET.get('id')
        if resource_id is None:
            form = SignUpForm()
            flag = False
            return render(request, 'minivideo/signup.html', {'form':form,'flag':flag})

        flag = True
        resource = get_object_or_404(Resource, pk=resource_id)

        perm = True
        if not request.user.has_perm('minivideo.manager'):
            if not 'stuno' in request.session:
                return HttpResponseRedirect( reverse('minivideo:login') )
            else:
                if request.session['stuno'] != resource.team_captain_stuno:
                    perm = False

        form = CommitForm(instance=resource)

        url = 'http://v.youku.com/v_show/id_(.*?).html'
        req = re.compile(url)
        number = re.search(req, resource.video_link)
        if number:
            number = number.group(1)
            
        return render(request, 'minivideo/signup.html', {'form':form,'flag':flag,'resource':resource,'number':number,'personal_perm':perm})

    def post(self, request):
        resource_id = request.GET.get('id')
        if resource_id is None:
            form = SignUpForm(request.POST)
            flag = False
            if not form.is_valid():
                return render(request, 'minivideo/signup.html', {'form':form,'flag':flag})
            form.save()
            return HttpResponseRedirect(reverse('minivideo:resource_list'))
        flag = True
        resource = Resource.objects.get(team_captain_stuno=request.POST['team_captain_stuno'])
        form = CommitForm(request.POST,request.FILES,instance=resource)
        if not form.is_valid():
            return render(request, 'minivideo/signup.html', {'form':form,'flag':flag})
        resource.has_verified = False
        form.save()
        return HttpResponseRedirect( reverse('minivideo:details')+'?id='+str(resource.id) )


def resource_list(request):
    resources = Resource.objects.all().order_by('has_verified','id')
    page = request.GET.get('page')
    paginator = Paginator(resources,15)
    try:
        page_list = paginator.page(page)
    except PageNotAnInteger:
        page_list = paginator.page(1)
    except EmptyPage:
        page_list = paginator.page(paginator.num_pages)

    return render(request,'minivideo/list.html',{ 'page_list':page_list})


@check_perms('minivideo.manager')
def verify(request):
    resource_id = request.GET.get('id')
    resource = get_object_or_404(Resource,pk=resource_id)
    resource.has_verified = not resource.has_verified
    resource.save()
    return HttpResponseRedirect(reverse('minivideo:resource_list'))


def index(request):
    resources = Resource.objects.all().filter(has_verified=True).order_by('pk')
    return render(request,'minivideo/index.html',{'resources':resources})


def details(request):
    resource_id = request.GET.get('id')
    resource = get_object_or_404(Resource,pk=resource_id)

    url = 'http://v.youku.com/v_show/id_(.*?).html'
    req = re.compile(url)
    number = re.search(req, resource.video_link)
    if number:
        number = number.group(1)
    return render(request,'minivideo/details.html',{'resource':resource, 'number' : number})


@check_perms('minivideo.manager')
def resource_delete(request):
    resource_id = request.GET.get('id')
    resource = get_object_or_404(Resource,pk=resource_id)
    resource.delete()
    return HttpResponseRedirect(reverse('minivideo:resource_list'))


class LoginView(View):
    
    def get(self, request):
        if 'stuno' in request.session:
            return HttpResponseRedirect(reverse('minivideo:resource_list'))
        form = loginForm()
        return render(request,'minivideo/login.html',{'form':form})

    def post(self, request):
        form = loginForm(request.POST)
        if not form.is_valid():
            return render(request, 'minivideo/login.html', {'form':form})
        request.session['stuno'] = request.POST['team_captain_stuno']
        request.session.set_expiry(0)
        return HttpResponseRedirect(reverse('minivideo:resource_list'))


def votes(request):
    resource_id = request.GET.get('id')
    resource = get_object_or_404(Resource, pk=resource_id)
    url = 'http://v.youku.com/v_show/id_(.*?).html'
    req = re.compile(url)
    number = re.search(req, resource.video_link)
    if number:
        number = number.group(1)
    ticket = request.GET.get('ticket')
    CASserver = 'https://auth.szu.edu.cn/cas.aspx/'
    ReturnURL = 'http://stu.szu.edu.cn/minivideo/votes/'

    if ticket:
        response = requests.get('%sserviceValidate?ticket=%s&service=%s?id=%s'%(CASserver, ticket, ReturnURL, resource_id)).content
        xp1 = ('/cas:serviceResponse/cas:authenticationSuccess/cas:attributes/cas:StudentNo')
        xp2 = ('/cas:serviceResponse/cas:authenticationSuccess/cas:attributes/cas:ICAccount')
        tree = etree.fromstring(response)
        request.session['stu_no'] = tree.xpath(xp1,  namespaces={'cas': 'http://www.yale.edu/tp/cas'})[0].text
        request.session['stu_ic'] = tree.xpath(xp2,  namespaces={'cas': 'http://www.yale.edu/tp/cas'})[0].text
        request.session.set_expiry(0)
        return HttpResponseRedirect('/minivideo/details/?id=%s' %resource_id)

    else:
        if 'stu_no' in request.session: 
            if len(Vote.objects.filter(stu_no=request.session['stu_no'])) < 2:
                if not Vote.objects.filter(stu_no=request.session['stu_no'], voted_id=resource.id):
                    v = Vote(stu_no=request.session['stu_no'], stu_ic=request.session['stu_ic'], voted_id=resource_id)
                    v.save()
                    resource.votes +=1
                    resource.save()
                    Msg = "投票成功，多谢您的支持！"
                else:
                    Msg = "您已投过该作品"
            else:
                Msg = "您已投过两次"
            
            return render(request,'minivideo/details.html',{'resource':resource, 'number' : number, 'Msg':Msg})

        else:
            return HttpResponseRedirect('%slogin?service=%s?id=%s' %(CASserver,  ReturnURL, resource_id))