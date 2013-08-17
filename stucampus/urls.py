from django.conf.urls import patterns, include, url

from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', 'stucampus.master.views.index', name='home'),
    url(r'^lost_and_found/', include('stucampus.lost_and_found.urls',
                                     namespace='lost_and_found')),
    url(r'^lecture/', include('stucampus.lecture.urls',
                              namespace='lecture')),
    url(r'^admin/', include(admin.site.urls)),
)


handler404 = 'stucampus.master.views.page_not_found'
