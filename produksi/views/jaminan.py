# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from produksi.models import Jaminan
from django.views import generic

# Create your views here.
class JaminanIndex(generic.ListView):
	template_name = "jaminan/index.html"
	context_object_name = "list-data"
	
	def get_queryset(self):
		return Jaminan.objects.filter(unit=self.request.user.profil.unit).all()
