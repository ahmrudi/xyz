from django import forms
from sia.models import Arsip, ArsipMasuk, ArsipKeluar, Brankas
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Reset, Column, Row

class BrankasForm(forms.ModelForm):
	class Meta:
		model = Brankas
		fields = ['kode', 'keterangan', 'status']
		
	def __init__(self, *args, **kwargs):
		super(BrankasForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			'nomor_dokumen',
			'nomor_brankas', 'keterangan',
			'jenis', 'divisi', 'unit', 'tipe',
			ButtonHolder(Submit('simpan', 'Simpan'), Reset('reset', 'Reset'))
		)
		
class ArsipForm(forms.ModelForm):
	class Meta:
		model = Arsip
		fields = ['nomor_dokumen', 'nomor_brankas', 'keterangan', 'jenis', 'divisi', 'unit', 'tipe']
		
	def __init__(self, *args, **kwargs):
		super(ArsipForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			'nomor_dokumen',
			'nomor_brankas', 'keterangan',
			'jenis', 'divisi', 'unit', 'tipe',
			ButtonHolder(Submit('simpan', 'Simpan'), Reset('reset', 'Reset'))
		)
		
class ArsipMasukForm(forms.ModelForm):
	class Meta:
		model = ArsipMasuk
		fields = ['yang_menyerahkan', 'yang_menerima', 'yang_mengetahui']
		
	def __init__(self, *args, **kwargs):
		super(ArsipMasukForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			'yang_menyerahkan', 'yang_menerima', 'yang_mengetahui',
			ButtonHolder(Submit('simpan', 'Simpan'), Reset('reset', 'Reset'))
		)
		
class ArsipKeluarForm(forms.ModelForm):
	class Meta:
		model = ArsipKeluar
		fields = ['yang_menyerahkan', 'yang_menerima', 'yang_mengetahui']
		
	def __init__(self, *args, **kwargs):
		super(ArsipKeluarForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			'yang_menyerahkan', 'yang_menerima', 'yang_mengetahui',
			ButtonHolder(Submit('simpan', 'Simpan'), Reset('reset', 'Reset'))
		)