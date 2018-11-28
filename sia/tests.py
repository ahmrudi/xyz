# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from datetime import datetime
from sia.models import *

# Create your tests here.
class TestArsip(TestCase):

	def test_arsip(self):
		arsip = Arsip()
		arsip.nomor_brankas = 1
		arsip.unit = "PST"
		arsip.divisi = "AKTG"
		arsip.jenis = "DOK"
		arsip.dibuat_oleh_id = 0
		arsip.save()
		
		self.assertEqual("DOK/AKTG/PST/11/2018", arsip.make_kode())
		
		arsip.tgl_dibuat = datetime(2018, 8, 1)
		arsip.save()
		
		self.assertEqual("DOK/AKTG/PST/08/2018", arsip.make_kode())