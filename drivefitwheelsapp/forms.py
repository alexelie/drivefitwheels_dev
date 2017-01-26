from django import forms
import re
class SetupForm(forms.Form):
	wheel_size_choice=(
		(15,"15\""),
		(16,"16\""),
		(17,"17\""),
		(18,"18\""),
		(19,"19\""),
		(20,"20\""),
		(21,"21\""),
	)
	width_choice=(
		(6.0,"6.0"),
		(6.5,"6.5"),
		(7.0,"7.0"),
		(7.5,"7.5"),
		(8.0,"8.0"),
		(8.5,"8.5"),
		(9.0,"9.0"),
		(9.5,"9.5"),
		(10.0,"10.0"),
		(10.5,"10.5"),
		(11.0,"11.0"),
		(11.5,"11.5"),
		(12.0,"12.0"),
	)
	year=forms.IntegerField()
	
	f_wheelsize=forms.ChoiceField(choices=wheel_size_choice)
	f_width=forms.ChoiceField(choices=width_choice)
	f_offset=forms.IntegerField()
	f_tiresize=forms.CharField(max_length=10)
	
	r_wheelsize=forms.ChoiceField(choices=wheel_size_choice)
	r_width=forms.ChoiceField(choices=width_choice)
	r_offset=forms.IntegerField()
	r_tiresize=forms.CharField(max_length=10)
	
	suspension=forms.BooleanField(required=False, initial=False)
	suspensionInfo=forms.CharField(max_length=100,required=False)
	spacer=forms.BooleanField(required=False,initial=False)
	spacerInfo=forms.CharField(max_length=100,required=False)
	fab=forms.BooleanField(required=False,initial=False)
	fabInfo=forms.CharField(max_length=100,required=False)
	img1=forms.ImageField()
	img2=forms.ImageField(required=False)
	img3=forms.ImageField(required=False)
	img4=forms.ImageField(required=False)
	
	def clean_tiresize(self):
		sizeField=self.cleaned_data['tiresize']
		tirematch=re.match(r'([0-9]{3})/([0-9]{2})/([0-9]{2})$', sizeField)
		if tirematch is None:
			raise forms.ValidationError("Please enter a valid format for 'Tire size' field")
			
		
class SearchForm(forms.Form):
	year_from=forms.IntegerField(required=False)
	year_to=forms.IntegerField(required=False)
	offset=forms.IntegerField(required=False)
	tire_size=forms.CharField(max_length=9,required=False)
	
	def clean_tire_size(self):
		sizeField=self.cleaned_data['tire_size']
		if sizeField=="":
			return
		tirematch=re.match(r'([0-9]{3})/([0-9]{2})/([0-9]{2})$', sizeField)
		if tirematch is None:
			raise forms.ValidationError("Please enter a valid format for 'Tire size' field")
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
