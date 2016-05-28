#-*- coding: utf-8
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.core.paginator import InvalidPage, Paginator

from stucampus.carousels.models import Slide
from stucampus.account.permission import check_perms
from stucampus.carousels.forms import SlideForm
from stucampus.articles.models import Article

class addSlide(View):
    @method_decorator(check_perms('carousels.slide_add'))
    def get(self, request):
        article_id = request.GET.get('id')
        fast = request.GET.get('fast')
        if fast == 'True':
            article = Article.objects.get(id=article_id)
            slide = Slide()
            slide.title = article.title
            slide.describe = article.summary
            slide.cover = article.cover
            slide.jumpUrl = '/articles/'+article_id+'/'
            slide.author = request.user
            slide.modifier = request.user
            slide.save()
            return HttpResponseRedirect(reverse('carousels:manage'))
        form = SlideForm()
        return render(request, 'carousels/carousel-form.html',
                {'form': form, 'post_url': reverse('carousels:add')})

    @method_decorator(check_perms('carousels.slide_add'))
    def post(self, request):
        form = SlideForm(request.POST,request.FILES )
        if not form.is_valid():
            return render(request, 'carousels/carousel-form.html',
                    {'form': form, 'post_url': reverse('carousels:add')})
        slide = form.save(commit=False)
        slide.author = request.user
        slide.modifier = request.user
        slide.save()
        return HttpResponseRedirect(reverse('carousels:manage'))

class ModifySlide(View):

    @method_decorator(check_perms('carousels.slide_add'))
    def get(self, request):
        slide_id = request.GET.get('id')
        slide = get_object_or_404(Slide, pk=slide_id)
        form = SlideForm(instance=slide)
        page = request.GET.get('page')
        return render(request, 'carousels/carousel-form.html',
                {'form': form, 'slide_id': slide_id, 'page': page,
                 'slide':slide, 'post_url': reverse('carousels:modify')})

    @method_decorator(check_perms('carousels.slide_add'))
    def post(self, request):
        slide_id = request.GET.get('id')
        slide = get_object_or_404(Slide, pk=slide_id)
        form = SlideForm(request.POST,request.FILES,instance=slide)
        page = request.GET.get('page')
        if not form.is_valid():
            return render(request, 'carousels/carousel-form.html',
                {'form': form, 'slide_id': slide_id,
                 'post_url': reverse('carousels:modify')})
        slide = form.save(commit=False)
        slide.modifier = request.user
        slide.save()
        return HttpResponseRedirect(reverse('carousels:manage')+'?page='+page)

@check_perms('carousels.slide_add')
def manage(request):
    editor = request.user
    pageid = request.GET.get('page')
    if editor.has_perm('carousels.slide_manage'):
        slide_list = Slide.objects.all()
    else:
        slide_list = Slide.objects.filter(author=editor)
    paginator = Paginator(
            slide_list.filter(deleted=False).order_by('-pk'), 10)
    try:
        page = paginator.page(pageid)
    except InvalidPage:
        pageid=1
        page = paginator.page(1)
    return render(request, 'carousels/manage.html',
            {'page': page , 'pageid': pageid})

@check_perms('carousels.slide_manage')
def publish(request):
    slide_id = request.GET.get('id')
    slide = get_object_or_404(Slide, pk=slide_id)
    slide.published = not slide.published
    slide.save()
    return HttpResponseRedirect(reverse('carousels:manage'))


@check_perms('carousels.slide_add')
def del_slide(request):
    slide_id = request.GET.get('id')
    slide = get_object_or_404(Slide, pk=slide_id)
    editor = request.user
    if editor.has_perm('carousels.slide_manage'):
        slide.deleted = not slide.deleted
    else:
        if editor == slide.author:
            slide.deleted = not slide.deleted
    slide.save()
    return HttpResponseRedirect(reverse('carousels:manage'))


