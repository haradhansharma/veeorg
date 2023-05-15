import re
from django.conf import settings
from .models import ExSite    
from django.core.cache import cache
from .models import *
from .menus import (
    category_menus,
    page_menus,
    footer_menu,
    header_menu,

)

def site_data():
    data = cache.get('site_data')
    if data is not None:
        return data

    site = ExSite.on_site.get()
    data = {
        'name' : site.site.name,
        'domain' : site.site.domain,
        'description': site.site_description,
        'author' : site.site.domain,
        'meta_tag' : site.site_meta_tag,
        'favicon': site.site_favicon.url,
        'mask_icon': site.mask_icon.url,
        'logo': site.site_logo.url,
        'slogan': site.slogan,
        'og_image': site.og_image.url,
        'facebook_link': site.facebook_link,
        'twitter_link': site.twitter_link, 
        'linkedin_link': site.linkedin_link,   
    }

    cache.set('site_data', data, timeout=3600)

    return data


def str_list_frm_path(request):   
    path = request.path

    # Split the path at each special character using a regular expression
    path_segments = re.split(r'[-_&/]', path)

    # Remove any empty strings from the list of path segments
    path_segments = [s for s in path_segments if s]
    return path_segments



def core_con(request):
    
        
        
    context = {   
        'category_menus' : category_menus(request),
        'page_menus' : page_menus(request),
        'footer_menu' : footer_menu(request),
        'header_menu' : header_menu(request),
        'site_data' : site_data(),
        'str_list_frm_path' : str_list_frm_path(request)
 
     
    }
    
    return context