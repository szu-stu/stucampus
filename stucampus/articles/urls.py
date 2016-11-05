from django.conf.urls import url, patterns

from stucampus.articles.views import AddView, ModifyView
from stucampus.articles.views import manage
from stucampus.articles.views import del_article, set_important, publish
from stucampus.articles.views import CategoryView

from stucampus.articles.views import article_list, article_display
from stucampus.articles.views import sharewechat

urlpatterns = [
    url(r'^manage/?$', manage, name='manage'),
    url(r'^add/?$', AddView.as_view(), name='add'),
    url(r'^modify/?$', ModifyView.as_view(), name='modify'),

    url(r'^del_article/?$', del_article, name='del_article'),
    url(r'^set_important/?$', set_important, name='set_important'),
    url(r'^publish/?$', publish, name='publish'),

    url(r'^category/?$',
            CategoryView.as_view(), name='category'),

    url(r'^(?P<category>\D*)/$', article_list, name='list'),
    url(r'^(?P<id>\d*)/?$', article_display, name='display'),
    url(r'^sharewechat/?', sharewechat, name='sharewechat'),
]
