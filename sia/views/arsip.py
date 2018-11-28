# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic, View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from easy_pdf import views as pdf_views
from sia.models import Arsip, ArsipMasuk, ArsipKeluar
from sia.forms import ArsipForm, ArsipMasukForm, ArsipKeluarForm

# Create your views here.
class PageTemplate(LoginRequiredMixin):
	def get_context_data(self, *args, **kwargs):
		data = super(PageTemplate, self).get_context_data(*args, **kwargs)
		data['title'] = self.title
		return data
		
class ArsipIndex(PageTemplate, generic.ListView):
	template_name = "index.html"
	context_object_name = "data"
	paginate_by = 5
	ordering_by = ['-tgl_diubah']
	title = "Data Arsip"
		
	def get_queryset(self, *args, **kwargs):
		return Arsip.objects.all()
		
class ArsipBaru(PageTemplate, generic.edit.CreateView):
	template_name = "form.html"
	form_class = ArsipForm
	title = "Tambah Arsip"
	
	def form_valid(self, form):
		form.instance.dibuat_oleh = self.request.user
		obj = form.save()
		arsip = ArsipMasuk(arsip=obj)
		arsip.dibuat_oleh = self.request.user
		arsip.save()
		arsip.make_kode()
		arsip.save()
		return super(ArsipBaru, self).form_valid(form)

class ArsipUbah(PageTemplate, generic.edit.UpdateView):
	template_name = "form.html"
	form_class = ArsipForm
	model = Arsip
	title = "Ubah Arsip"
		
class ArsipMasukView(PageTemplate, generic.DetailView):
	template_name = "detail.html"
	model = Arsip
	title = "Detail Arsip"
	
	def get_context_data(self, **kwargs):
		context = super(ArsipMasukView, self).get_context_data(**kwargs)
		arsip = self.get_object()
		form = ArsipMasukForm(instance=arsip.penerimaan)
		context['form']=form
		return context

class ArsipKeluarView(LoginRequiredMixin, generic.DetailView):
	template_name = "detail.html"
	model = Arsip
	
	def get_context_data(self, **kwargs):
		context = super(ArsipKeluarView, self).get_context_data(**kwargs)
		arsip = self.get_object()
		form = ArsipKeluarForm(instance=arsip.pengembalian)
		context['form']=form
		return context
		
class PenerimaanArsip(PageTemplate, generic.View):
	template_name = "detail.html"
	title = "Detail Arsip"
	
	def get(self, request, *args, **kwargs):
		view = ArsipMasukView.as_view()
		return view(request, *args, **kwargs)
		
	def post(self, request, *args, **kwargs):
		view = ArsipMasukUbah.as_view()
		return view(request, *args, **kwargs)
		
class PengembalianArsip(generic.View):
	template_name = "detail.html"
	
	def get(self, request, *args, **kwargs):
		view = ArsipKeluarView.as_view()
		return view(request, *args, **kwargs)
		
	def post(self, request, *args, **kwargs):
		view = ArsipKeluarUbah.as_view()
		return view(request, *args, **kwargs)
	
class ArsipMasukUbah(LoginRequiredMixin, generic.edit.UpdateView):
	template_name = "form.html"
	form_class = ArsipMasukForm
	model = ArsipMasuk
	
	def get_object(self, *args, **kwargs):
		return ArsipMasuk.objects.get(arsip_id=self.kwargs.get('pk'))
		
	def form_valid(self, form):
		form.instance.arsip.status = 1
		form.instance.arsip.save()
		return super(ArsipMasukUbah, self).form_valid(form)
		
	def get_success_url(self):
		return reverse('arsip:terima-detail', kwargs={'pk_arsip':self.object.arsip.pk, 'pk':self.object.pk})
		
class ArsipKeluarUbah(LoginRequiredMixin, generic.edit.UpdateView):
	template_name = "form.html"
	form_class = ArsipKeluarForm
	model = ArsipKeluar
	
	def get_object(self, *args, **kwargs):
		return ArsipKeluar.objects.get(arsip_id=self.kwargs.get('pk'))
		
	def form_valid(self, form):
		form.instance.arsip.status = 1
		form.instance.arsip.save()
		return super(ArsipKeluarUbah, self).form_valid(form)
		
	def get_success_url(self):
		return reverse('arsip:terima-detail', kwargs={'pk_arsip':self.object.arsip.pk, 'pk':self.object.pk})

class ArsipMasukDetail(PageTemplate, generic.DetailView):
	template_name = "detail_penerimaan.html"
	model = ArsipMasuk
	title = "Penerimaan Arsip"
	
class ArsipKeluarBaru(LoginRequiredMixin, generic.edit.CreateView):
	template_name = "form.html"
	form_class = ArsipKeluarForm
	
	def form_valid(self, form):
		form.instance.dibuat_oleh = self.request.user
		form.instance.arsip = Arsip.objects.get(pk=self.kwargs.get('pk'))
		form.instance.arsip.status = 2
		form.instance.arsip.save()
		form.instance.make_kode()
		return super(ArsipKeluarBaru, self).form_valid(form)
		
class ArsipKeluarDetail(LoginRequiredMixin, generic.DetailView):
	template_name = "detail_penerimaan.html"
	model = ArsipKeluar
	
from django.conf import settings
class SuratPenerimaan(LoginRequiredMixin, pdf_views.PDFTemplateResponseMixin, generic.DetailView):
	template_name = "surat_penerimaan.html"
	model = ArsipMasuk
	base_url = 'file://{}/'.format(settings.STATIC_ROOT)
			
	def get_context_data(self, **kwargs):
		nomor = self.get_object().nomor
		return super(SuratPenerimaan, self).get_context_data(
			title=nomor, **kwargs
		)