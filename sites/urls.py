from django.conf.urls import url

from xyz import views

urlpatterns = [
	url(r'^$', views.construction, name='index'),
	url(r'^ubah-password/$', views.change_password, name='ubah_password'),
]