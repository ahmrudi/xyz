# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from uuid import uuid4

# Create your models here.
class Brankas(models.Model):
	kode = models.CharField("Kode", max_length=10)
	keterangan = models.TextField("Keterangan")
	status = models.IntegerField(default=0, choices=((0, 'Aktif'), (1, 'Pasif')))
	
	class Meta:
		db_table = "brankas"
		
	def __str__(self):
		return self.kode
	
class Arsip(models.Model):
	kode = models.UUIDField(default=uuid4, primary_key=True, editable=False)
	nomor_dokumen = models.CharField("Nomor Dokumen", max_length=50, unique=True)
	nomor_brankas = models.ForeignKey(Brankas, verbose_name="Nomor Brankas", on_delete=models.CASCADE)
	keterangan = models.TextField("Keterangan", default="")
	divisi = models.CharField("Divisi", max_length=4, choices=(("KEUN", "Keuangan"),
		("AKTG", "Akunting"),("PRDS", "Produksi"), ("MRTG", "Marketing"),
		("DRKS", "Direksi"), ("LGTK", "Logistik"), ("UMUM", "Umum")))
	unit = models.CharField("Unit", max_length=3, choices=(("PST", "Pusat"),
		("BGR", "Bogor"), ("KCC", "KaCiCa"), ("SCI", "SuCi"), ("RNK", "Rangkas")))
	jenis = models.CharField("Jenis Arsip", max_length=3, choices=(("DOK", "Dokumen"), ("JMN", "Jaminan"), ("BRG", "Barang")))
	tipe = models.IntegerField("Tipe Arsip", default=0, choices=((0, "Penting"), (1, "Rahasia"), (2, "Umum")))
	status = models.IntegerField("Status", default=0, choices=((0, "-"), (1, "Ada"), (2, "Diambil")))
	dibuat_oleh = models.ForeignKey(User, related_name="arsip", on_delete=models.CASCADE)
	tgl_dibuat = models.DateTimeField(auto_now_add=True)
	tgl_diubah = models.DateTimeField(auto_now=True)
	
	def make_kode(self):
		bln = str(self.tgl_dibuat.month)
		if len(bln) == 1:
			bln = "0" + bln
		else:
			bln = bln
		kd = [self.jenis, self.divisi, self.unit, bln, str(self.tgl_dibuat.year)]
		return "/".join(kd)
	
	class Meta:
		db_table = "arsip"
		
	def get_absolute_url(self):
		return reverse("arsip:detail", kwargs={'pk':str(self.pk)})
		
	def __str__(self):
		return str(self.kode)
		
class ArsipMasuk(models.Model):
	nomor = models.CharField("Nomor", max_length=20, unique=True, editable=False, default="")
	arsip = models.OneToOneField("arsip", related_name="penerimaan", on_delete=models.CASCADE)
	yang_menyerahkan = models.CharField("Yang Menyerahkan", max_length=50)
	yang_menerima = models.CharField("Yang Menerima", max_length=50)
	yang_mengetahui = models.CharField("Yang Mengetahui", max_length=50)
	dibuat_oleh = models.ForeignKey(User, related_name="arsip_masuk", on_delete=models.CASCADE)
	tgl_dibuat = models.DateTimeField(auto_now_add=True)
	tgl_diubah = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = "arsip_masuk"
		
	def __str__(self):
		return self.nomor

	def make_kode(self):
		bln = str(self.tgl_dibuat.month)
		if len(bln) == 1:
			bln = "0" + bln
		else:
			bln = bln
		kd = [self.arsip.jenis, self.arsip.divisi, self.arsip.unit, bln, str(self.tgl_dibuat.year)]
		kd = "/".join(kd)
		kode = str(self.pk)
		nol = 5 - len(kode)
		self.nomor = "0" * nol + kode + "/MSK/" + kd
		
class ArsipKeluar(models.Model):
	nomor = models.CharField("Nomor", max_length=20, unique=True, editable=False, default="")
	arsip = models.OneToOneField("arsip", related_name="penyerahan", on_delete=models.CASCADE)
	yang_menyerahkan = models.CharField("Yang Menyerahkan", max_length=50)
	yang_menerima = models.CharField("Yang Menerima", max_length=50)
	yang_mengetahui = models.CharField("Yang Mengetahui", max_length=50)
	dibuat_oleh = models.ForeignKey(User, related_name="arsip_keluar", on_delete=models.CASCADE)
	tgl_dibuat = models.DateTimeField(auto_now_add=True)
	tgl_diubah = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = "arsip_keluar"
		
	def save(self, *args, **kwargs):
		self.arsip.status = 2
		return super(ArsipKeluar, self).save(*args, **kwargs)
		
	def __str__(self):
		return self.nomor
		
	def make_kode(self):
		kode = str(ArsipKeluar.objects.count()+1)
		nol = 5 - len(kode)
		self.nomor = "0" * nol + kode + "/KLR/" + self.arsip.make_kode()