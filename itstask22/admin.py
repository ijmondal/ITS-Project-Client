# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
#from .models import *

def register(self,model_or_iterable,admin_class=None,**options):
	l=[models.HouseHolds,models.Wells,models.Yields,models.Members,models.Farms]
# Register your models here.
	admin.site.register(l)

