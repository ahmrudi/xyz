"""baze URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from sia import views

urlpatterns = [
	url(r'^$', views.ArsipIndex.as_view(), name="index"),
	url(r'^baru/$', views.ArsipBaru.as_view(), name="baru"),
	url(r'^(?P<pk>[\w-]+)/$', views.PenerimaanArsip.as_view(), name="detail"),
	url(r'^(?P<pk>[\w-]+)/ubah/$', views.ArsipUbah.as_view(), name="ubah"),
	url(r'^(?P<pk_arsip>[\w-]+)/(?P<pk>[0-9])/$', views.ArsipMasukDetail.as_view(), name="terima-detail"),
	url(r'^(?P<pk_arsip>[\w-]+)/(?P<pk>[0-9])/penerimaan/$', views.SuratPenerimaan.as_view(), name='surat-penerimaan'),
]
