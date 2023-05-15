from django import forms
from .models import CvLibrary
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox

class CVForm(forms.ModelForm):
    captcha = ReCaptchaField(label='', widget=ReCaptchaV2Checkbox)  
    class Meta:
        model = CvLibrary
        fields = '__all__'
        
        
        widgets = {                      
            'name_and_surename': forms.TextInput(attrs={'name':'name_and_surename', 'class':'form-control', 'aria-label':'Full Name', 'placeholder': 'e. g. Jone Doe' }),
            'current_profession': forms.TextInput(attrs={'name':'current_profession', 'class':'form-control', 'aria-label':'Profession', 'placeholder': 'e. g. Web Developer'}),
            'job_title_applying_for': forms.TextInput(attrs={'name':'job_title_applying_for', 'class':'form-control', 'aria-label':'Job Title', 'placeholder': 'e. g. Web Developer' }),
            'email_address': forms.EmailInput(attrs={'name':'email', 'class':'form-control', 'aria-label':'Email', 'placeholder': 'e. g. jone@doe.com' }),
            'cv_file': forms.FileInput(attrs={'name': 'cv_file', 'class':'form-control', 'aria-label':'CV', 'placeholder': 'Upload your CV PDF only'})
            
            
        }