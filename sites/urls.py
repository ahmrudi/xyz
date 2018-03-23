from django.conf.urls import url

from xyz import views

urlpatterns = [
	url(r'^$', views.construction, name='index'),
]