from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from drivefitwheelsapp.forms import SetupForm
from drivefitwheelsapp.forms import SearchForm
from django.template import RequestContext
from django.views.generic import TemplateView
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageOps
import datetime
import pdb

from .models import Car
from .models import CarImg
# Register your models here.
admin.site.register(Car)
admin.site.register(CarImg)

class drivefitwheelsAdmin(AdminSite):

     def get_urls(self):
         from django.conf.urls import url
         urls = super(drivefitwheelsAdmin, self).get_urls()
         urls += [
             url(r'^addsetup/$', self.admin_view(AddSetup.as_view()))
         ]
         return urls

     def driveitadmin(self, request):
         return HttpResponse("Hello!")

admin_site = drivefitwheelsAdmin()
	
class AddSetup(TemplateView):
	template_name='adminaddSetup.html'	
	
	def post(self,request,*args,**kwargs):
		form=SetupForm(request.POST,request.FILES)
		if form.is_valid():

			if 'suspension' in request.POST:
				boxsuspension=True
				suspinfo=form.data['suspensionInfo']
			else:
				boxsuspension=False
				suspinfo=""
				
			if 'spacer' in request.POST:
				boxspacer=True
				spacerinfo=form.data['spacerInfo']
			else:
				boxspacer=False
				spacerinfo=""
				
			if 'fab' in request.POST:
				boxfab=True
				fabinfo=form.data['fabInfo']
			else:
				boxfab=False
				fabinfo=""
							
			carObj=Car(
					brand=request.POST['brand'],
					model=request.POST['model'],
					year=form.cleaned_data['year'],
					
					f_wheelsize=form.cleaned_data['f_wheelsize'],
					f_width=form.cleaned_data['f_width'],
					f_offset=form.cleaned_data['f_offset'],
					f_tiresize=form.data['f_tiresize'],
					
					r_wheelsize=form.cleaned_data['r_wheelsize'],
					r_width=form.cleaned_data['r_width'],
					r_offset=form.cleaned_data['r_offset'],
					r_tiresize=form.data['r_tiresize'],
					
					suspension=boxsuspension,
					suspensionInfo=suspinfo,
					spacer=boxspacer,
					spacerInfo=spacerinfo,
					fab=boxfab,
					fabInfo=fabinfo,
					email=request.POST['email'],
					date=datetime.date.today(),
					valid=False
			)
			#save car entry
			carObj.save();
			
			#loop images
			for filename, file in request.FILES.iteritems():			

				#==========THUMBNAIL RESIZE==============
				size=(135, 90)
				basewidth = 138
				#resize image to crop later in center
				thumbData = Image.open(form.cleaned_data[filename])
				wpercent = (basewidth/float(thumbData.size[0]))
				hsize = int((float(thumbData.size[1])*float(wpercent)))
				thumbData = thumbData.resize((basewidth,hsize), Image.ANTIALIAS)
				
				#cropping center of img with size
				half_the_width = thumbData.size[0] / 2
				half_the_height = thumbData.size[1] / 2
				thumbData = thumbData.crop(
					(
						half_the_width - int(size[0]/2),
						half_the_height - int(size[1]/2),
						half_the_width + int(size[0]/2),
						half_the_height + int(size[1]/2)
					)
				)
				
				#in memory thumbnail img to save in model
				thumb_io = StringIO.StringIO()
				thumbData.save(thumb_io, format='JPEG')
				thumb_file = InMemoryUploadedFile(thumb_io, None,  request.FILES[filename].name+'_tumb.jpg', 'image/jpeg', thumb_io.len, None)				
				#==========END THUMBNAIL RESIZE==============
				
				#==========LARGE IMG RESIZE==============
				basewidth = 900
				mainImgData = Image.open(form.cleaned_data[filename])
				wpercent = (basewidth/float(mainImgData.size[0]))
				hsize = int((float(mainImgData.size[1])*float(wpercent)))
				mainImgData = mainImgData.resize((basewidth,hsize), Image.ANTIALIAS)
				
				#in memory thumbnail img to save in model
				mainImg_io = StringIO.StringIO()
				mainImgData.save(mainImg_io, format='JPEG')
				mainImg_file = InMemoryUploadedFile(mainImg_io, None,  request.FILES[filename].name+'_main.jpg', 'image/jpeg', mainImg_io.len, None)								
				#==========END LARGE IMG RESIZE==============
				
				carImg = CarImg(					
					car = carObj,
					img = mainImg_file,
					thumb = thumb_file
				)
				
				carImg.save()
				
			return HttpResponseRedirect('/drivefitwheelsadmin/addsetup/')
		return render(request,'addSetup.html',{'form':form})
		
	def get_context_data(self,**kwargs):
		context=super(AddSetup,self).get_context_data(**kwargs)
		context['form']=SetupForm()
		return context		 
		 

