
from django.urls import path, include
from .views import *
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *
from django.views.generic.base import TemplateView


app_name = 'core'

sitemap_list = {
    'static': StaticSitemap,
    'pages' : PageSitemap,
    'category' : CategorySitemap,
    'BlogSitemap' : BlogSitemap
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemap_list}, name='django.contrib.sitemaps.views.sitemap'),      
    path('', home, name='home'),
    path('b/<str:slug>/', blog_detail, name='blog_details'),
    path('b/<str:slug>/htmx', hta, name='hta'),       
    path('like_or_dislike/<int:content_type_id>/<int:object_id>/', like_or_dislike, name='like_or_dislike'),    
    path('category/<str:slug>', category_detail, name='category_detail'),    
    path('p/<str:slug>/', page_detail, name='page_detail'),   
    path('job/success/', success, name='success'),
  

    
]

urlpatterns += [
    path('template/humansunfolio/', human_sun_home, name='human_sun_home'),
    path('template/humansunfolio/<str:webp>/', human_sun_home, name='human_sun_home_pages'),
    
]
