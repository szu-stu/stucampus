from django.conf.urls import patterns, include, url

from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', 'stucampus.master.views.front.index', name='home'),
    url(r'^aboutus$', 'stucampus.master.views.front.about_us', name='aboutus'),
    url(r'^manage/', include('stucampus.master.urls', namespace='master')),
    url(r'^account/', include('stucampus.account.urls', namespace='account')),
    url(r'^organization/', include('stucampus.organization.urls',
                                   namespace='organization')),
    url(r'^infor/', include('stucampus.infor.urls', namespace='infor')),
    url(r'^lost_and_found/', include('stucampus.lost_and_found.urls',
                                     namespace='lost_and_found')),
    url(r'^lecture/', include('stucampus.lecture.urls',
                              namespace='lecture')),
    url(r'^spider/', include('stucampus.spider.urls', namespace='spider')),
    url(r'^admin/', include(admin.site.urls)),
)


handler404 = 'stucampus.master.views.front.page_not_found'
