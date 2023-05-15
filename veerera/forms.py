from django import forms
from django.contrib.auth.forms import (    
    AuthenticationForm,
    PasswordResetForm,
    PasswordChangeForm,
    SetPasswordForm
    ) 

from django.utils.translation import gettext_lazy as _

class CustomAuthenticationForm(AuthenticationForm):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({ 'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        
class CustomPasswordResetForm(PasswordResetForm):  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
    #     self.email = forms.EmailField(
    #     label=_("Email"),
    #     max_length=254,
    #     widget=forms.EmailInput(attrs={"autocomplete": "email", 'class': 'form-control'}),
    # )
        

        
class CustomPasswordChangeForm(PasswordChangeForm):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({ 'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
        
        
        
class CustomSetPasswordForm(SetPasswordForm):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
        