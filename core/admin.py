from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin


class ExtendSiteOfSite(admin.StackedInline):
    model = ExSite
    can_delete = False   

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')
    inlines = [ExtendSiteOfSite]    
admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)

class PageAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('body',)
    prepopulated_fields = {'slug': ('title',)}
    
    def save_model(self, request, obj, form, change):
        # set the flag indicating saving from admin
        obj._saving_from_admin = True        
        super().save_model(request, obj, form, change)
        obj._saving_from_admin = False    
admin.site.register(Page, PageAdmin)





class BlogAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('body',)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'status',)
    
    def save_model(self, request, obj, form, change):       
        # set the flag indicating saving from admin
        obj._saving_from_admin = True        
        super().save_model(request, obj, form, change)
        obj._saving_from_admin = False      
    
    
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        # Get the parent instance
        instance = form.instance
        
        
        latest_links = Blog.published.exclude(id=instance.id).order_by('-id')
        latest_indicator_links = latest_links[:6]
        latest_table_links = latest_links[6:12]
        instance.build_indicator_link.add(*latest_indicator_links)
        instance.build_table_link.add(*latest_table_links)
    

admin.site.register(Blog, BlogAdmin)






class CategoryAdmin(admin.ModelAdmin):     
    
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['title', 'parent__title']
    search_fields = ['title' ]
    list_display = ('title', 'id',)
admin.site.register(Category, CategoryAdmin)


class CvLibraryAdmin(admin.ModelAdmin):     
    
    # prepopulated_fields = {'slug': ('title',)}
    list_filter = ['current_profession', 'job_title_applying_for' ]
    search_fields = ['current_profession', 'job_title_applying_for', 'name_and_surename' ]
    list_display = ('name_and_surename', 'email_address','current_profession','job_title_applying_for')
admin.site.register(CvLibrary, CvLibraryAdmin)

admin.site.register(ResponseBackup)
admin.site.register(Action)
