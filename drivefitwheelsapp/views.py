import smtplib
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.template import loader,Context
from django.views.generic import TemplateView
from django import forms
from django.shortcuts import render
from django.db.models import Q
import datetime
from django.conf import settings
from drivefitwheelsapp.models import Car
from drivefitwheelsapp.models import CarImg
from drivefitwheelsapp.forms import SetupForm
from drivefitwheelsapp.forms import SearchForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from email.utils import COMMASPACE, formatdate
from PIL import Image
import pdb
# Create your views here.


class Home(TemplateView):
	def get(self,request,*args,**kwargs):
		if request.is_ajax():
			carId=request.GET.get('id','')
			carImg=CarImg.objects.filter(car_id=carId)
			carObj=Car.objects.get(id=carId)
			t=loader.get_template('ajax_info.html')
			c=Context({'carInfo':carObj,'carImg':carImg})
			return HttpResponse(t.render(c))
		context=super(Home,self).get_context_data(**kwargs)
		if 'succeed' in context:
			succeed='Succeed'
		else:
			succeed=''
			
		if 'page' in request.GET:
			page=request.GET.get('page')
		else:
			page=1;
		
		result=Car.objects.filter(valid=True)
		result=result.order_by('-id')
		pages=Paginator(result,10)
		try:
			currentPage=pages.page(page)
		except PageNotAnInteger:
			currentPage=pages.page(1)
		except EmptyPage:
			currentPage=pages.page(pages.num_pages)
			
		return render(request,'recent.html',{'cars':currentPage,'form':SearchForm,'succeed':succeed,'currentPage':currentPage})
	def get_context_data(self,**kwargs):
		context=super(Home,self).get_context_data(**kwargs)
		context['form']=SearchForm
		return context	
		
class Search(TemplateView):
	def get(self,request,*args,**kwargs):
		form=SearchForm(request.GET)
		#pdb.set_trace()	
		if form.is_valid():

			result=Car.objects.filter(valid=True)
	
			if 'page' in request.GET:
				page=request.GET.get('page')
			else:
				page=1;
			
			if request.GET.get('brand','')!='All':
				result=result.filter(brand=request.GET.get('brand',''))
				if request.GET.get('model','')!='All':
					result=result.filter(model=request.GET.get('model',''))
			if request.GET.get('year_from')!='':
				result=result.filter(year__gte=int(float(request.GET.get('year_from',''))))
			if request.GET.get('year_to')!='':
				result=result.filter(year__lte=int(float(request.GET.get('year_to',''))))
			
			#wheels
			if request.GET.get('wheel_size','')!='All':
				result=result.filter(Q(f_wheelsize=request.GET.get('wheel_size')) | Q(r_wheelsize=request.GET.get('wheel_size')))
			if request.GET.get('wheel_width','')!='All':
				result=result.filter(Q(f_width=request.GET.get('wheel_width')) | Q(r_width=request.GET.get('wheel_width')))
			if request.GET.get('offset','')!='':
				result=result.filter(Q(f_offset=int(float(request.GET.get('offset')))) | Q(r_offset=int(float(request.GET.get('offset')))))
			if request.GET.get('tire_size','')!='':
				result=result.filter(Q(f_tiresize=request.GET.get('tire_size')) | Q(r_tiresize=request.GET.get('tire_size')))
						
			result=result.order_by('date')		
			
			return render(request,'search.html',{'cars':result,'form':SearchForm})
		
		page=1
		result=[]
		pages=Paginator(result,10)
		try:
			currentPage=pages.page(page)
		except PageNotAnInteger:
			currentPage=pages.page(1)
		except EmptyPage:
			currentPage=pages.page(pages.num_pages)		
		#return render(request,'recent.html',{'cars':currentPage,'form':SearchForm, 'error':form.errors, 'currentPage':currentPage})
		return render(request,'search.html',{'cars':currentPage,'form':SearchForm,'error':form.errors, 'currentPage':currentPage})
	
class Succeed(TemplateView):
	template_name='succeed.html'
	def get_context_data(self,**kwargs):
		context=super(Succeed,self).get_context_data(**kwargs)
		context['form']=SetupForm()
		return context
		
class AddSetup(TemplateView):
	template_name='addSetup.html'
	
	
	def sendEmailForUploadVerification(self, email, carInfoModel, carImgs):
		emailFrom = email
		emailTo = "XXXX"
		subject = "drivefitwheels: Car entry validation"
		text = "Car info:" + "<br/>"
		text +=	"Brand: "+carInfoModel.brand + "<br/>"
		text += "Model: "+carInfoModel.model + "<br/>"
		text +=	"Year: "+str(carInfoModel.year) + "<br/>"
		
		text +=	"Front wheelsize: "+str(carInfoModel.f_wheelsize) + "<br/>"
		text +=	"Front width: "+str(carInfoModel.f_width) + "<br/>"
		text +=	"Front offset: "+str(carInfoModel.f_offset) + "<br/>"
		text +=	"Front tiresize: "+carInfoModel.f_tiresize + "<br/>"

		text +=	"Rear wheelsize: "+str(carInfoModel.r_wheelsize) + "<br/>"
		text +=	"Rear width: "+str(carInfoModel.r_width) + "<br/>"
		text +=	"Rear offset: "+str(carInfoModel.r_offset) + "<br/>"
		text +=	"Rear tiresize: "+carInfoModel.r_tiresize + "<br/>"
		
		text +=	"Suspension: "+str(carInfoModel.suspension) + "<br/>"
		text +=	"SuspensionInfo: "+carInfoModel.suspensionInfo + "<br/>"
		text +=	"Spacer: "+str(carInfoModel.spacer) + "<br/>"
		text +=	"SpacerInfo: "+carInfoModel.spacerInfo + "<br/>"
		text +=	"Fab: "+str(carInfoModel.fab) + "<br/>"
		text +=	"FabInfo: "+carInfoModel.fabInfo + "<br/>"
		text +=	"Date: "+str(carInfoModel.date) + "<br/>"
		text +=	"Email: "+str(carInfoModel.email) + "<br/>"
			
		self.sendEmail(emailFrom, emailTo, subject, text, carImgs)
		
	def sendEmail(self, send_from, send_to, subject, text, files=None):

		fromaddr = send_from
		toaddr = send_to
		 
		msg = MIMEMultipart()		 
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject'] = subject
		 
		body = text
		 
		msg.attach(MIMEText(body, 'html'))
		
		for file in files:
			filename = file.name
			attachment = file.read()			 
			part = MIMEBase('application', 'octet-stream')
			part.set_payload(attachment)
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment; filename= %s" % filename)			 
			msg.attach(part)
							 
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(toaddr, "XXXX")
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()
	
	
	def post(self,request,*args,**kwargs):
		form=SetupForm(request.POST,request.FILES)
		if form.is_valid():
			if 'suspension' in request.POST:
				boxsuspension=request.POST.get('suspension', 'default')
				suspinfo=request.POST.get('suspensionInfo', 'default')
			else:
				boxsuspension=False
				suspinfo=""
			if 'spacer' in request.POST:
				boxspacer=request.POST.get('spacer', 'default')
				spacerinfo=request.POST.get('spacerInfo', 'default')
			else:
				boxspacer=False
				spacerinfo=""
			if 'fab' in request.POST:
				boxfab=request.POST.get('fab', 'default')
				fabinfo=request.POST.get('fabInfo', 'default')
			else:
				boxfab=False
				fabinfo=""
							
			car=Car(
					brand=request.POST.get('brand', 'default'),
					model=request.POST.get('model', 'default'),
					year=request.POST.get('year', 'default'),
					
					f_wheelsize=request.POST.get('f_wheelsize', 'default'),
					f_width=request.POST.get('f_width', 'default'),
					f_offset=request.POST.get('f_offset', 'default'),
					f_tiresize=request.POST.get('f_tiresize', 'default'),
					
					r_wheelsize=request.POST.get('r_wheelsize', 'default'),
					r_width=request.POST.get('r_width', 'default'),
					r_offset=request.POST.get('r_offset', 'default'),
					r_tiresize=request.POST.get('r_tiresize', 'default'),
					
					suspension=boxsuspension,
					suspensionInfo=suspinfo,
					spacer=boxspacer,
					spacerInfo=spacerinfo,
					fab=boxfab,
					fabInfo=fabinfo,
					date=datetime.date.today(),
					email=request.POST.get('email', 'default'),
					valid=False
			)
			email=request.POST.get('email', 'default')
			imgList=list()
			for filename, file in request.FILES.iteritems():
				imgList.append(file)
						
			self.sendEmailForUploadVerification(email, car, imgList)

			return HttpResponseRedirect('/drivefitwheels/succeed/')
			
		return render(request,'/',{'form':form})
		
	def get_context_data(self,**kwargs):
		context=super(AddSetup,self).get_context_data(**kwargs)
		context['form']=SetupForm()
		return context
		

		
class CarImgContainer:

	def __init__(self, imgName, imgData, imgContentType):
		self.imgName=imgName
		self.imgData=imgData
		self.imgContentType=imgContentType
		
