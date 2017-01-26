from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Car(models.Model):
	brand=models.CharField(max_length=100)
	model=models.CharField(max_length=100)
	year=models.IntegerField()
	
	f_wheelsize=models.IntegerField()
	f_width=models.FloatField()
	f_offset=models.IntegerField()
	f_tiresize=models.CharField(max_length=(10))
	
	r_wheelsize=models.IntegerField(null=True)
	r_width=models.FloatField(null=True)
	r_offset=models.IntegerField(null=True)
	r_tiresize=models.CharField(max_length=(10), null=True)
	
	suspension=models.BooleanField(blank=True)
	suspensionInfo=models.CharField(max_length=70,blank=True)
	spacer=models.BooleanField(blank=True)
	spacerInfo=models.CharField(max_length=70,blank=True)
	fab=models.BooleanField(blank=True)
	fabInfo=models.CharField(max_length=70,blank=True)
	date=models.DateField()
	valid=models.BooleanField()
	email=models.EmailField(max_length=70,blank=True)

	def __unicode__(self):
		return self.brand+" "+self.model
			
class CarImg(models.Model):
	car=models.ForeignKey(Car);
	img=models.ImageField(upload_to='images/')
	thumb=models.ImageField(upload_to='images/thumbnails/')
	def __unicode__(self):
		return self.img.name
	def delete(self,*args,**kwargs):
		self.img.delete(False)
		self.thumb.delete(False)
		super(CarImg,self).delete(*args,**kwargs)
	

		
