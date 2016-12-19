"""chrimas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from stucampus.christmas import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^exchange/', views.ExchangeView.as_view(), name="exchange"),
    url(r'^given/', views.GivenView.as_view(), name="given"),
    url(r'^giftList/', views.giftList, name="giftList"),
    url(r'^$', views.index, name="index"),
    url(r'^giftResult/', views.resultList, name="giftResult"),
    url(r'^postWantType', views.postWantType, name="postWantType"),
    url(r'^manage/$', views.manageIndex, name="manage"),
    url(r'^manage/gift', views.manageGift.as_view(), name="giftmanage"),
    url(r'^manage/user', views.manageUser.as_view(), name="usermanage"),
    url(r'^manage/get', views.manageGet, name="getmanage"),
    url(r'^read/$', views.ReadView.as_view(), name="read"),
    url(r'^changeMyInfo/$', views.changeMyInfo, name="changeinfo"),
    url(r'^readDetail/$', views.ReadDetailView.as_view(), name='readDetail'),
    url(r'^makeExcel/$', views.makeExcel.as_view(), name='makeExcel'),
    url(r'^makeResultExcel/$', views.makeResultExcel.as_view(), name='makeResultExcel'),
    url(r'^makeFinalExcel/$', views.makeFinalExcel.as_view(), name='makeFinalExcel'),
]
