import os

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^$', 'stucampus.master.views.front.index', name='home'),
    url(r'^aboutus$', 'stucampus.master.views.front.about_us', name='aboutus'),
    url(r'^manage/', include('stucampus.master.urls', namespace='master')),
    url(r'^account/', include('stucampus.account.urls', namespace='account')),
    url(r'^organization/', include('stucampus.organization.urls',
                                   namespace='organization')),
    #url(r'^infor/', include('stucampus.infor.urls', namespace='infor')),
    url(r'^articles/', include('stucampus.articles.urls',
                                namespace='articles')),
    url(r'^magazine/', include('stucampus.magazine.urls',
                                namespace='magazine')),
    url(r'^lecture/', include('stucampus.lecture.urls',
                              namespace='lecture')),
    url(r'^activity/', include('stucampus.activity.urls',
                               namespace='activity')),
    url(r'^szuspeech/', include('stucampus.szuspeech.urls',
                               namespace='szuspeech')),
    url(r'^minivideo/', include('stucampus.minivideo.urls',
                               namespace='minivideo')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^spider/', include('stucampus.spider.urls', namespace='spider')),
    url(r'^dreamer/', include('stucampus.dreamer.urls', namespace='dreamer')),
)

# serve media file when using developing server
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT,}),
        url(r'^pdfjs/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(settings.ROOT, 'stucampus',
                                           'static', 'pdfjs'),}),
        )


handler404 = 'stucampus.master.views.front.page_not_found'
