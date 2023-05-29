from pprint import pprint
from django.apps import apps
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.module_loading import import_string
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.templatetags.static import static
# from core.models import (
#     Category
# )
from core.helper import (
    pages,
    categories,
    model_with_field,

)
from django.contrib import admin




def category_menus(request):
    all_cat = categories().filter(add_to_cat_menu = True, sites__id = request.site.id) 
    menu_items = []
    for cat in all_cat:
        if cat.have_items:         
            item_dict = {
                'title' : cat.title,
                'url' : cat.get_absolute_url(),
                'data_set': False,
                'icon' : cat.icon
                
            }
            menu_items.append(item_dict)
        
    return menu_items

def page_menus(request):
    all_page = pages().filter(add_to_page_menu = True, sites__id = request.site.id)
    menu_items = []
    for p in all_page:
        item_dict = {
            'title' : p.title,
            'url' : p.get_absolute_url(), 
            'data_set': False  
        }
        menu_items.append(item_dict)        
    return menu_items




def footer_menu(request):
    # Get objects of models where add_to_menu is True
    objects_with_footer_menu = []

    for model in model_with_field('add_to_footer_menu'):
        objects_with_footer_menu += model.objects.filter(add_to_footer_menu=True, sites__id = request.site.id).order_by('title')
        
    menu_items = []  
    for obj in objects_with_footer_menu:
        item_dict = {
            'title' : obj.title,
            'url' : obj.get_absolute_url(),  
            'data_set': False 
        }
        menu_items.append(item_dict)     
    if request.user.is_authenticated and request.user.is_superuser:
        menu_items.append(
            {'title': 'Create Blog', 'url': reverse('createblog:createblog_home'),'data_set': False},        
            ) 
   
    if not request.user.is_authenticated:   
        
        menu_items.append(
            {'title': 'Login', 'url': reverse('login'),'data_set': False},        
            ) 
        
        
    return menu_items

def header_menu(request):
    # Get objects of models where add_to_menu is True
    objects_with_header_menu = []

    for model in model_with_field('add_to_header_menu'):
        objects_with_header_menu += model.objects.filter(add_to_header_menu=True, sites__id = request.site.id).order_by('title')
        
    menu_items = [] 
    menu_items.append(
        {'title': 'Home', 'url': '/', 'data_set': False},        
        )  
    menu_items.append(
        {'title': 'Page', 'url': False, 'data_set': page_menus(request) },        
        ) 
    for obj in objects_with_header_menu:
        if getattr(obj, 'have_items'):
            if obj.have_items:             
                item_dict = {
                    'title' : obj.title,
                    'url' : obj.get_absolute_url(), 
                    'data_set': False  
                }
                menu_items.append(item_dict)            
       

        
    
        
    return menu_items



    



    