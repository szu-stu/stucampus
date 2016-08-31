import os

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve as static_serve

from DjangoUeditor import urls as django_urls

from stucampus.master import urls as master_urls
from stucampus.account import urls as account_urls
from stucampus.organization import urls as organization_urls
from stucampus.articles import urls as articles_urls
from stucampus.magazine import urls as magazine_urls
from stucampus.lecture import urls as lecture_urls
from stucampus.activity import urls as activity_urls
from stucampus.szuspeech import urls as szuspeech_urls
from stucampus.minivideo import urls as minivideo_urls
from stucampus.spider import urls as spider_urls
from stucampus.FreeTimeCount import urls as FreeTimeCount_urls
from stucampus.carousels import urls as carousels_urls
from stucampus.master.views.front import index,about_us
from stucampus.member_infor import urls as member_infor_url
from stucampus.summer_plans import urls as summer_plans_url


admin.autodiscover()


urlpatterns = [
    url(r'^ueditor/', include(django_urls)),
    url(r'^$', index, name='home'),
    url(r'^aboutus$',about_us, name='aboutus'),
    url(r'^manage/', include(master_urls, namespace='master')),
    url(r'^account/', include(account_urls, namespace='account')),
    url(r'^organization/', include(organization_urls,
                                   namespace='organization')),
    #url(r'^infor/', include('stucampus.infor.urls', namespace='infor')),
    url(r'^articles/', include(articles_urls,
                                namespace='articles')),
    url(r'^magazine/', include(magazine_urls,
                                namespace='magazine')),
    url(r'^lecture/', include(lecture_urls,
                              namespace='lecture')),
    url(r'^activity/', include(activity_urls,
                               namespace='activity')),
    url(r'^szuspeech/', include(szuspeech_urls,
                               namespace='szuspeech')),
    url(r'^minivideo/', include(minivideo_urls,
                               namespace='minivideo')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^spider/', include(spider_urls, namespace='spider')),
    url(r'^carousels/', include(carousels_urls, namespace='carousels')),
    url(r'^dreamer/', include('stucampus.dreamer.urls', namespace='dreamer')),
	url(r'^freetimecount/', include(FreeTimeCount_urls,namespace='FreeTimeCount')),
    url(r'^member_infor/', include(member_infor_url,namespace='member_infor')),
    url(r'^summer_plans/', include(summer_plans_url,namespace='summer_plans')),

]

#serve media file when using developing server
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', static_serve,
            {'document_root': settings.MEDIA_ROOT,}),
        url(r'^pdfjs/(?P<path>.*)$', static_serve,
            {'document_root': os.path.join(settings.ROOT, 'stucampus',
                                           'static', 'pdfjs'),}),
        ]


handler404 = 'stucampus.master.views.front.page_not_found'
