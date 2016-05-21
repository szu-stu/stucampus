from django.conf.urls import url, patterns

from stucampus.carousels.views import addSlide, ModifySlide
from stucampus.carousels.views import manage
from stucampus.carousels.views import  publish, del_slide


urlpatterns = [
    url(r'^manage/$', manage, name='manage'),
    url(r'^add/$', addSlide.as_view(), name='add'),
    url(r'^modify/$', ModifySlide.as_view(), name='modify'),
    url(r'^del_slide/$', del_slide, name='delete'),
    url(r'^publish/$', publish, name='publish'),
]
