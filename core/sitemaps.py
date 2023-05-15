from django.contrib import sitemaps
from django.urls import reverse
from .models import *
from django.conf import settings
from django.utils import timezone
from django.db.models import Count





class StaticSitemap(sitemaps.Sitemap):
    priority = 1
    changefreq = 'monthly'

    def items(self):
        return ['core:home'] 
    
    def lastmod(self, obj):
        return timezone.now()
        
    def location(self, item):
        return reverse(item)   
    
class PageSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.8    

    def items(self):
        return Page.objects.filter(status = 'published')[:10]
    
    def lastmod(self, obj):
        return obj.created_at
        
    def location(self, obj):
        return obj.get_absolute_url()
    
class CategorySitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.7    

    def items(self):
        categories_with_blogs = Category.objects.filter(
            is_active=True
        ).annotate(
            blog_count=Count('blogs_category')
        ).filter(
            blog_count__gt=0
        )
        categories = [category for category in categories_with_blogs if category.blog_count > 0]
        return categories
    
    def lastmod(self, obj):
        return obj.created_at
        
    def location(self, obj):
        return obj.get_absolute_url()
    
class BlogSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.5    

    def items(self):
        blogs = Blog.objects.filter(status = 'published', should_as_it_is=True)[:10]
        return blogs
    
    def lastmod(self, obj):
        return obj.created_at
        
    def location(self, obj):
        return obj.get_absolute_url()
    

    

    

    

    

               
    