#-*- coding: utf-8
from django.shortcuts import render
from django.core.paginator import InvalidPage, Paginator

from stucampus.articles.models import Article, Category
from stucampus.lecture.models import LectureMessage
from stucampus.activity.models import ActivityMessage
from stucampus.utils import DuoShuo


def index(request):
    if not request.is_ajax():
        # 深大焦点

        important_articles = \
                Article.objects.filter(
                        publish=True,
                        deleted=False,
                        important=True).order_by('-pk')[:5]
        # 不同类别的文章
        article_dict = \
                ((category, \
                Article.objects.filter(
                    publish=True,
                    deleted=False,
                    category=category).order_by('-pk')[:5]) \
                for category in Category.objects.all().order_by('priority'))
        lecture_list = \
                LectureMessage.objects.filter(checked=True).order_by('-pk')[:7]
        activity_list = \
                ActivityMessage.objects.filter(checked=True).order_by('-pk')[:7]
        comments = DuoShuo.getRecentComment()
        visitors = DuoShuo.getListVisitors()
        important_articles=DuoShuo.appendNumToArticles(important_articles)
    
        return render(request, "index.html",
                    {'important_articles': important_articles,
                    'article_dict': article_dict,
                    'lecture_list': lecture_list,
                    'activity_list': activity_list,
                    'comments':comments,
                    'visitors':visitors})
    else:
        article_list = Article.objects.filter(publish=True,deleted=False).order_by('-pk')
        paginator = Paginator(article_list, 5)
        try:
            important_articles = paginator.page(request.GET.get('page'))
        except InvalidPage:
            important_articles = paginator.page(1)
        
        return render(request, "ajax_article_list.html",{'important_articles':important_articles})


def about_us(request):
    return render(request, "aboutus.html")


def page_not_found(request):
    return render(request, "404.html")
