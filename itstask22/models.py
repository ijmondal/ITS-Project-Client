# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from decimal import Decimal
import datetime


class HouseHolds(models.Model):
	ID=models.IntegerField(primary_key=True)
	Monthly_Income=models.FloatField(null=True, blank=True, default=300.00)
	Location_Id=models.PointField(default = 'POINT(1 1)')
	
	
		
class Members(models.Model):
	ID=models.IntegerField(primary_key=True)
	HouseHold_Id=models.ForeignKey('HouseHolds',on_delete=models.CASCADE,default=1)
	Name=models.CharField(max_length=10)
	DOB=models.DateTimeField()
	Gender=models.CharField(max_length=1)
	


class Farms(models.Model):
	ID=models.IntegerField(primary_key=True)
	Area=models.DecimalField(max_digits=20,decimal_places=5)
	HouseHold_Id=models.ForeignKey('HouseHolds',on_delete=models.CASCADE,default=1)



class Wells(models.Model):
	ID=models.IntegerField(primary_key=True)
	#Point_Id=models.ForeignKey('Points',on_delete=models.CASCADE,default=1)
	Depth=models.DecimalField(max_digits=20,decimal_places=5)
	
	

