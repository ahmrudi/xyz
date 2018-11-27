from django.conf.urls import url
from produksi import views
urlpatterns = [
	url(r'^$', views.JaminanIndex.as_view(), name="index"),
]