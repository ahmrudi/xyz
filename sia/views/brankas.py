# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic, View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from easy_pdf import views as pdf_views
from sia.models import Brankas
from sia.forms import BrankasForm

# Create your views here.
class BrankasIndex(LoginRequiredMixin, generic.ListView):
	template_name = "index.html"
	context_object_name = "data"
	paginate_by = 5
	ordering_by = ['-tgl_diubah']
		
	def get_queryset(self, *args, **kwargs):
		return Brankas.objects.all()
		
class BrankasBaru(LoginRequiredMixin, generic.edit.CreateView):
	template_name = "form.html"
	form_class = BrankasForm

class BrankasUbah(LoginRequiredMixin, generic.edit.UpdateView):
	template_name = "form.html"
	form_class = BrankasForm
	model = Brankas