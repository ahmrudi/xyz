# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4

# Create your models here.
class UnitUser(models.Model):
	unit = models.CharField("Nama Unit", max_length=10, unique=True)
	class Meta:
		db_table = "unit"
		
	def __str__(self):
		return self.unit
		
class Profil(models.Model):
	user = models.OneToOneField(User, related_name="profil", on_delete=models.CASCADE)
	unit = models.OneToOneField(UnitUser, related_name="profil", on_delete=models.CASCADE)
	
	class Meta:
		db_table = "profil"
		
	def __str__(self):
		return self.user.username
		
class Jaminan(models.Model):
	id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
	unit = models.CharField("Unit", default="", max_length=10)
	kode = models.CharField("Kode", default="", max_length=50, unique=True)
	nik_peternak = models.CharField("NIK Peternak", default="", max_length=16)
	nama_peternak = models.CharField("Nama Peternak", default="", max_length=16)
	alamat_peternak = models.TextField("Alamat Peternak", default="")
	jenis = models.CharField("Jenis Jaminan", default="", max_length=50)
	atas_nama = models.CharField("Atas Nama", default="", max_length=50)
	keterangan = models.TextField("Atas Nama", default="")
	menyerahkan = models.CharField("Yang Menyerahkan", default="", max_length=50)
	menerima = models.CharField("Yang Menerima", default="", max_length=50)
	mengetahui = models.CharField("Yang Mengetahui", default="", max_length=50)
	tanggal = models.DateField("Tanggal", default=timezone.now)
	tgl_dibuat = models.DateTimeField(auto_now_add=True)
	tgl_diubah = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = "jaminan"
		
	def __str__(self):
		return self.kode
