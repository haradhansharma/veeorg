
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView, 
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView

    )
from django.http import HttpResponseRedirect, JsonResponse 
from .forms import (
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm
)
from core.context_processor import site_data

import logging
log = logging.getLogger('log')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        site = site_data()
        site['name'] = 'Password Rest Complete'
        context['site_data'] = site
        
        return context     
        
    template_name = 'registration/password_reset_complete.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):     
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        site = site_data()
        site['name'] = 'Password Reset Sent'
        context['site_data'] = site
        
        return context     
        
    template_name = 'registration/password_reset_done.html'

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        site = site_data()
        site['name'] = 'Login'
        context['site_data'] = site        
        return context             
    template_name = 'registration/login.html'
    
class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        site = site_data()
        site['name'] = 'Password Change'
        context['site_data'] = site
        
        return context
    template_name = 'registration/password_change_form.html'
    
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        site = site_data()
        site['name'] = 'Password Reset'
        context['site_data'] = site
        return context
    
    template_name = 'registration/password_reset_form.html'
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        site = site_data()
        site['name'] = 'Password Rest Confirm'
        context['site_data'] = site
        return context
        
    template_name = 'registration/password_reset_confirm.html'
    
def webmanifest(request):
    site = site_data()      
    icons = []    
    ic192 = {
        "src": site.get('og_image'),
        "sizes": "192x192",
        "type": "image/png"        
    }
    
    icons.append(ic192)   
    ic512 = {
        "src": site.get('og_image'),
        "sizes": "512x512",
        "type": "image/png"        
    }
    icons.append(ic512)    
    data = {
        'name' : site['name'],
        'short_name' : site['name'],
        'icons' : icons,        
        "theme_color": "#ffffff",
        "background_color": "#ffffff",
        "display": "standalone"        
    }
    
    return JsonResponse(data, safe=False)

def page_not_found(request, exception):
    log.error(f"404 error: {request.META.get('HTTP_REFERER', 'unknown')} - {request.path}")
    return HttpResponseRedirect('/')