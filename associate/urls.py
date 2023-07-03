
from django.urls import path, include
from .views import *



app_name = 'associate'



urlpatterns = [ 
    path('picked-essentials/', picked_essentials, name='picked_essentials'),

    
    
    
]
