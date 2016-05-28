#-*- coding: utf-8
import sys
import xlrd
import datetime

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import InvalidPage, Paginator
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Member
from .forms import MemberForm,MemberListForm
from .utils import getdate
from stucampus.account.permission import check_perms

from login_szu import login_szu

sys.setdefaultencoding( "utf-8" )


# Create your views here.

class SearchMember(View):
    @login_szu
    def get(self,request):
        if Member.objects.filter(szu_no=request.session['szu_no'],approved=True).exists():
            return render(request, 'member_infor/search_form.html')
        else:
            return render(request,'member_infor/login_fail.html')

    @login_szu
    def post(self,request):
        if not Member.objects.filter(szu_no=request.session['szu_no'],approved=True).exists():
            return render(request, 'member_infor/login_fail.html')
        q = request.POST.get("q")
        students = Member.objects.filter(Q(name__contains=q)|Q(szu_no__contains=q)|Q(nick_name__contains=q))
        if students.exists():
            tips = None
        else:
            tips =u"没有相关信息"
        return render(request,'member_infor/search_form.html',{'students':students,'tips':tips})

class AddMember(View):

    @method_decorator(check_perms('member_infor.member_add'))
    def get(self,request):
        form = MemberForm()
        title = u"添加通讯录成员信息"
        return render(request,'member_infor/member_form.html',{'form':form,'post_url': reverse('member_infor:add'),'title':title})

    @method_decorator(check_perms('member_infor.member_add'))
    def post(self,request):
        form = MemberForm(request.POST)
        title = u"添加通讯录成员信息"
        if not form.is_valid():
            return render(request, 'member_infor/member_form.html',
                {'form': form, 'post_url': reverse('member_infor:add'),'title':title})
        member = form.save(commit=False)
        member.approved = True
        member.save()
        return HttpResponseRedirect(reverse('member_infor:manage'))

class AddMemberList(View):
    '''
        批量添加通讯录成员,添加的成员默认通过
    '''

    @method_decorator(check_perms('member_infor.member_add'))
    def get(self,request):
        form = MemberListForm()
        title = u"通过xlsx批量添加通讯录信息"
        tips = u'''只支持上传xlsx文件，第一列为姓名，第二列为学号，第三列为电话号码,这三列为必须,后三列生日，邮箱，昵称，为非必须，你可以按顺序添写，无信息的那列放空白即可，
                    文件第一行为标签栏，填写姓名，学号，电话号码，生日，邮箱，昵称
                    第二列开始才是具体个人信息,
                    如陈泽集，2014150122,15889674306,1994-08-10,649743466@qq.com,阿集
                    如果学号已经存在，则会更新原来的信息
                    如果文件的某一处格式不符合规范，则会跳转单独更改，错误信息后面的信息需要再次添加
                '''
        return render(request,'member_infor/member_form.html',{'form':form,'post_url': reverse('member_infor:add_list'),"title":title,"tips":tips})

    @method_decorator(check_perms('member_infor.member_add'))
    def post(self,request):
        form = MemberListForm(request.POST,request.FILES)
        
        if not form.is_valid():
            title = u"通过xlsx批量添加通讯录信息"
            tips = u'''只支持上传xlsx文件，第一列为姓名，第二列为学号，第三列为电话号码,这三列为必须,后三列生日，邮箱，昵称，为非必须，你可以按顺序添写，无信息的那列放空白即可，
                    文件第一行为标签栏，填写姓名，学号，电话号码，生日，邮箱，昵称
                    第二列开始才是具体个人信息,
                    如陈泽集，2014150122,15889674306,1994-08-10,649743466@qq.com,阿集
                    如果学号已经存在，则会更新原来的信息
                    如果文件的某一处格式不符合规范，则会跳转单独更改，错误信息后面的信息需要再次添加
                '''
            return render(request, 'member_infor/member_form.html',
                {'form': form, 'post_url': reverse('member_infor:add_list'),"title":title,"tips":tips})
        file = form.cleaned_data.get('file')
        data = xlrd.open_workbook(file_contents = file.read(),encoding_override="utf-8")
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        title = u"修改批量上传中的错误信息"
        tips = u'''
                    该错误信息后面的信息将不会被添加，你可以修正完xlsx后，重新批量上传
                '''
        for rownum in range(1,nrows):
            row = table.row_values(rownum)
            szu_no = int (row[1])
            if Member.objects.filter(szu_no=szu_no).exists():
                member = get_object_or_404(Member, szu_no=szu_no)
                form = MemberForm({'name':row[0],'szu_no': int(row[1]),'mobile_phone_number': int(row[2]),'birthday':getdate(row[3]),'e_mail':row[4],'nick_name':row[5]},instance=member)
                if not form.is_valid():
                    return render(request, 'member_infor/member_form.html',
                        {'form': form, 'post_url': reverse('member_infor:add'),"title":title,"tips":tips})
                member = form.save(commit=False)
                member.approved = True
                member.save()
            else:
                form = MemberForm({'name':row[0],'szu_no': int(row[1]),'mobile_phone_number': int(row[2]),'birthday':getdate(row[3]),'e_mail':row[4],'nick_name':row[5]})
                if not form.is_valid():
                    return render(request, 'member_infor/member_form.html',
                        {'form': form, 'post_url': reverse('member_infor:add'),"title":title,"tips":tips})
                member = form.save(commit=False)
                member.approved = True
                member.save() 
        file.close()
        return HttpResponseRedirect(reverse('member_infor:manage'))



class ModifyMember(View):
    '''
        管理员修改信息
    '''
    @method_decorator(check_perms('member_infor.member_add'))
    def get(self, request):
        member_id = request.GET.get('id')
        member = get_object_or_404(Member, pk=member_id)
        form = MemberForm(instance=member)
        page = request.GET.get('page')
        title = u"修改通讯录信息"
        return render(request, 'member_infor/member_form.html',
                {'form': form, 'member_id': member_id, 'page': page,
                 'post_url': reverse('member_infor:modify'),'title':title})

    @method_decorator(check_perms('member_infor.member_add'))
    def post(self, request):
        member_id = request.GET.get('id')
        member = get_object_or_404(Member, pk=member_id)
        form = MemberForm(request.POST,instance=member)
        page = request.GET.get('page')
        title = u"修改通讯录信息"
        if not form.is_valid():
            return render(request, 'member_infor/member_form.html',
                {'form': form, 'member_id': member_id,
                 'post_url': reverse('member_infor:modify'),'title':title})
        form.save()
        return HttpResponseRedirect(reverse('member_infor:manage')+'?page='+page)

class UserModifyMember(View):
    '''
        用户自己修改自己的信息
    '''
    @login_szu
    def get(self,request):
        szu_no = request.session.get("szu_no")
        member = get_object_or_404(Member, szu_no=szu_no)
        form = MemberForm(instance=member)
        title = u"修改个人信息"
        return render(request, 'member_infor/modify_form.html',#need to write
                {'form': form, 'post_url': reverse('member_infor:user_modify_member'),'title':title})
    @login_szu
    def post(self,request):
        szu_no = request.session.get("szu_no")
        member = get_object_or_404(Member, szu_no=szu_no)
        form = MemberForm(request.POST,instance=member)
        title = u"修改个人信息"
        if not form.is_valid():
            return render(request, 'member_infor/modify_form.html',
                {'form': form,'post_url': reverse('member_infor:user_modify_member'),'title':title})
        member = form.save(commit=False)
        member.szu_no = request.session.get("szu_no")
        member.name = request.session.get("szu_name")
        member.save()
        return HttpResponseRedirect(reverse('member_infor:search'))

class ApplyMember(View):
    '''
        用户申请加入通讯录
    '''
    @login_szu
    def get(self,request):
        member = {
            'name':request.session.get("szu_name"),
            "szu_no":request.session.get("szu_no"),
        }
        form = MemberForm(member)
        title = u"申请加入通讯录"
        return render(request, 'member_infor/modify_form.html',
                {'form': form,'post_url': reverse('member_infor:apply'),'title':title})

    @login_szu
    def post(self,request):
        form = MemberForm(request.POST)
        title = u"申请加入通讯录"
        if not form.is_valid():
            return render(request, 'member_infor/modify_form.html',
                {'form': form,'post_url': reverse('member_infor:apply'),'title':title})
        form.save()
        return HttpResponseRedirect(reverse('member_infor:search'))




@check_perms('member_infor.member_add')
def manage(request):
    '''
        已经通过的名单，管理员添加的信息默认通过
    '''
    members = Member.objects.filter(approved=True).order_by("-pk")
    page_id = request.GET.get('page')
    paginator = Paginator(members,10)
    try:
        page = paginator.page(page_id)
    except InvalidPage:
        page_id=1
        page = paginator.page(1)
    return render(request, 'member_infor/manage.html',
            {'page': page , 'page_id': page_id})

@check_perms('member_infor.member_manage')
def pending_approve_members(request):
    '''
        申请加入的通讯录的名单
    '''
    members = Member.objects.filter(approved=False).order_by("-pk")
    page_id = request.GET.get('page')
    paginator = Paginator(members,10)
    try:
        page = paginator.page(page_id)
    except InvalidPage:
        page_id=1
        page = paginator.page(1)
    return render(request, 'member_infor/manage.html',
            {'page': page , 'page_id': page_id})

@check_perms('member_infor.member_manage')
def approve_member(request):
    '''
        批准通过
    '''
    member_id = request.GET.get('id')
    member = get_object_or_404(Member, pk=member_id)
    member.approved = True
    member.save()
    return HttpResponseRedirect(reverse('member_infor:pending_approve_members'))

@check_perms('member_infor.member_manage')
def del_member(request):
    member_id = request.GET.get('id')
    member = get_object_or_404(Member, pk=member_id)
    member.delete()
    return HttpResponseRedirect(reverse('member_infor:manage'))

