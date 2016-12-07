#-*- coding: utf-8
from django.shortcuts import render
from django.core.paginator import InvalidPage, Paginator

from stucampus.articles.models import Article, Category
from stucampus.lecture.models import LectureMessage
from stucampus.activity.models import ActivityMessage
from stucampus.utils import DuoShuo
from stucampus.carousels.models import Slide


def index(request):
    if not request.is_ajax():
        # 深大焦点
        slides = Slide.objects.filter(
                        published=True,
                        deleted=False).order_by("-priority","-pk")[:5]  
        # 最新文章
        newest_articles = \
                Article.objects.filter(
                        publish=True,
                        deleted=False).order_by('-pk')[:10]
        paginator = Paginator(newest_articles, 5)
        try:
            newest_articles = paginator.page(request.GET.get('page'))
        except InvalidPage:
            newest_articles = paginator.page(1)
        #newest_articles=DuoShuo.appendNumToArticles(newest_articles)
        
        #comments = DuoShuo.getRecentComment()
        #visitors = DuoShuo.getListVisitors()

        categories=Category.objects.all().order_by("priority")
          
        return render(request, "index.html",
                    {'slides': slides,
                    'newest_articles':newest_articles,
                    #'comments':comments,
                    #'visitors':visitors,
                    'categories':categories})
    else:
        article_list = Article.objects.filter(publish=True,deleted=False).order_by('-pk')
        paginator = Paginator(article_list, 5)
        try:
            newest_articles = paginator.page(request.GET.get('page'))
        except InvalidPage:
            newest_articles = paginator.page(1)
        #newest_articles=DuoShuo.appendNumToArticles(newest_articles)
        
        return render(request, "ajax_article_list.html",{'newest_articles':newest_articles})


def about_us(request):
    return render(request, "aboutus.html")


def page_not_found(request):
    return render(request, "404.html")
