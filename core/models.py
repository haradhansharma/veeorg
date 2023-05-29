
from django.db import models
from django.db.models import F
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import activate, gettext_lazy as _
from django.contrib.sites.managers import CurrentSiteManager
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from core.mixins import (
    TitleAndSlugModelMixin, 
    CreatorModelMixin,    
    SitesModelMixin,
    IsActiveModelMixin,
    MenuModelMixin,
    SaveFromAdminMixin,
    DateFieldModelMixin,
    ) 

from .agent_helper import get_client_ip, get_para_list_from

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Action(models.Model):
    VIEW = 'view'
    LIKE = 'like'
    ACTION_TYPES = (
        (VIEW, 'View'),
        (LIKE, 'Like')
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,db_index=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')   
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    action_type = models.CharField(max_length=4, choices=ACTION_TYPES, default=VIEW,db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)  
    
    

class Category(
    TitleAndSlugModelMixin, 
    CreatorModelMixin,    
    SitesModelMixin,
    IsActiveModelMixin,
    MenuModelMixin,
    DateFieldModelMixin,
    models.Model,
    SaveFromAdminMixin,
    
    ):
 
    icon = models.CharField(_('FA Icon'), max_length=250, help_text=_('HTML Fontawesoome icon'), default='<i class="fa-solid fa-calendar-check"></i>')
    description = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name=_('Parent'))        
    add_to_cat_menu = models.BooleanField(default=True)  
    

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')    
        ordering = ['-created_at'] 
        
    def get_absolute_url(self):
        return reverse('core:category_detail', args=[str(self.slug)])
    
    @property
    def have_items(self):
        if self.blogs_category.filter(status = 'published').exists() or self.pages_category.filter(status = 'published').exists():
            return True
        return False
        
    
    






class UserCMSManager(models.Manager):
    def foruser(self, user):
        # Filter pages based on the provided user
        return self.filter(creator=user)

class Page(   
    TitleAndSlugModelMixin, 
    IsActiveModelMixin,
    MenuModelMixin,
    SitesModelMixin,  
    CreatorModelMixin, 
    DateFieldModelMixin,
    models.Model,   
    SaveFromAdminMixin,
    
    ):  
    
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('published', _('Published')),
        ('unpublished', _('UnPublished')),        
    )
    
    categories = models.ManyToManyField(
        Category,
        blank=True,
        verbose_name=_('Categories'),
        related_name='pages_category'   
    )  
     
   
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name=_('Parent'))
    body = models.TextField(verbose_name=_('Body'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')   
    actions = GenericRelation(Action)
    objects = models.Manager()  # Fallback manager to query all pages
  
    
    # Manager for filtering pages based on user to call Page.userpages.foruser(request.user)
    userpages = UserCMSManager()
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:page_detail', args=[str(self.slug)])

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'        
        ordering = ['-created_at']
        
    def save(self, request=None, *args, **kwargs):          
        if getattr(self, '_saving_from_admin', False):           
            super().save(request, *args, **kwargs)
        else:        
            SaveFromAdminMixin.save(self, request=request, *args, **kwargs)     
            
            
    def view(self, request):
        # create a new action object for this view
        Action.objects.create(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk,
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
            action_type=Action.VIEW
        )       


    def like(self, request):
        Action.objects.create(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk,
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
            action_type=Action.LIKE
        )
        
    def dislike(self, request):
        Action.objects.get(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk,
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
            action_type=Action.LIKE
        ).delete()
        
    @property
    def total_view(self):
        total = Action.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk,
            action_type=Action.VIEW
        ).count()
        return total
    
    @property
    def total_like(self):
        total = Action.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk,
            action_type=Action.LIKE
        ).count()
        return total

        
 
        
        
    
        
        
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')
    
class UnPublishedManager(models.Manager):
    def get_queryset(self):
        return super(UnPublishedManager, self).get_queryset().filter(status='unpublished')
    
class DraftManager(models.Manager):
    def get_queryset(self):
        return super(DraftManager, self).get_queryset().filter(status='draft').order_by('-updated_at')
        
        
class Blog(
    TitleAndSlugModelMixin,
    MenuModelMixin,
    SitesModelMixin,
    CreatorModelMixin, 
    DateFieldModelMixin,
    SaveFromAdminMixin,
    
    models.Model,
    
    ):
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('published', _('Published')),
        ('unpublished', _('UnPublished')),        
    )
    
    feature = models.ImageField(_('Feature Image'), upload_to='blog/feature_image/')
    
    
    categories = models.ManyToManyField(
        Category,
        blank=True,
        db_index=True,
        verbose_name=_('Categories'),
        related_name='blogs_category'
      
    )  
    ref_link = models.URLField(default='/')
    
    body = models.TextField(verbose_name=_('Body'))  
      
    build_indicator_link = models.ManyToManyField('self', blank=True,  db_index=True, serialize=True, )
    
    build_table_link = models.ManyToManyField('self', blank=True,  db_index=True, serialize=True,)

    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)   
    actions = GenericRelation(Action)
    
    
    
    
    JOB_ZONE = {
        ('EU_COUNTRIES', 'EU_COUNTRIES'),
        ('AMERICAN_COUNTRIES', 'AMERICAN_COUNTRIES'),
        ('MIDDLEEAST_COUNTRIES', 'MIDDLEEAST_COUNTRIES'),
        ('ASIAN_COUNTRIES', 'ASIAN_COUNTRIES'),
        ('OCENIA_COUNTRIES', 'OCENIA_COUNTRIES'),
        ('AFRICAN_COUNTRIES', 'AFRICAN_COUNTRIES'),
        
    }
    job_area = models.CharField(max_length=20, choices=JOB_ZONE, default='EU_COUNTRIES')  
    
    EXTRA_BLOCKS = {
        ('JOB_POST', 'JOB_POST'),
        ('SALARY_RANGE_BLOCK', 'SALARY_RANGE_BLOCK'),   
    }    
    extra_blocks = models.CharField(max_length=20, choices=EXTRA_BLOCKS, default='JOB_POST')  
    
    should_have_hta = models.BooleanField(default=True, verbose_name="Should have How To Apply?")
    should_have_apf = models.BooleanField(default=True, verbose_name="Should have Application Form?")
    should_as_it_is = models.BooleanField(default=False, verbose_name="Should As it is As Body?")
    
    
    def view(self, request):
        # create a new action object for this view
        Action.objects.create(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk,
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
            action_type=Action.VIEW
        )       


    def like(self, request):
        Action.objects.create(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk,
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
            action_type=Action.LIKE
        )
        
    def dislike(self, request):
        Action.objects.get(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk,
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
            action_type=Action.LIKE
        ).delete()
        
        
    @property
    def total_view(self):
        total = Action.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk,
            action_type=Action.VIEW
        ).count()
        return total
    
    @property
    def total_like(self):
        total = Action.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk,
            action_type=Action.LIKE
        ).count()
        return total      
    
    
      
    @property  
    def get_content_type(self):
        return ContentType.objects.get_for_model(self)
    
    
    objects = models.Manager()#default manager
    published = PublishedManager()#Cutom Manager
    unpublished = UnPublishedManager()#Cutom Manager    
    draft = DraftManager()#Cutom Manager
    
    # Manager for filtering pages based on user to call Blog.userblogs.foruser(request.user)
    userblogs = UserCMSManager()
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:blog_details', args=[str(self.slug)])        
    
    def like_or_dislike_url(self):
        return reverse('core:like_or_dislike', args=[int(self.get_content_type.id), str(self.id)])        
    
    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        ordering = ['-created_at']
        
        
   
    def latest_indicator_links_blocks(self, para_len):
        para_len += 1 if para_len % 2 != 0 else 0
        latest_links = self.build_indicator_link.exclude(pk=self.pk)[:para_len]
        return self._create_link_blocks(latest_links, block_size=2)

    
    def build_table_link_blocks(self, para_len):
        para_len += 1 if para_len % 2 != 0 else 0
        latest_links = self.build_table_link.exclude(pk=self.pk)[:para_len]
        return self._create_link_blocks(latest_links, block_size=3)

    def _create_link_blocks(self, links, block_size):
        blocks = []
        current_block = []
        for link in links:
            current_block.append(link)
            if len(current_block) == block_size:
                blocks.append(current_block)
                current_block = []
        if current_block:
            blocks.append(current_block)
        return blocks
        
        
    def append_to_save(self, request=None, *args, **kwargs):  
             
        if not self.should_as_it_is:                                       
            len_of_para = len(get_para_list_from(self.body))           
            latest_links = Blog.published.exclude(id=self.id)       
            latest_indicator_links = latest_links[-len_of_para % 2:]
            latest_table_links = latest_links[-len_of_para % 2:len_of_para]
            self.build_indicator_link.add(*latest_indicator_links)
            self.build_table_link.add(*latest_table_links)
       
  
def validate_file_size(value):
    filesize= value.size

    if filesize > 5*1024*1024:
        raise ValidationError(_("The maximum file size that can be uploaded is 5MB"))
      
        
class CvLibrary(models.Model):
    name_and_surename = models.CharField(max_length=252)
    current_profession = models.CharField(max_length=252)
    job_title_applying_for = models.CharField(max_length=252)
    email_address = models.EmailField()
    cv_file = models.FileField(
        verbose_name='Upload your CV PDF only',
        upload_to='cv_files/', 
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'], message='Only PDF allowed'),
            validate_file_size
            ]
        )
    
    def __str__(self):
        return self.name_and_surename
    
    
    
class ExSite(models.Model):    
    site = models.OneToOneField(Site, primary_key=True, verbose_name='site', on_delete=models.CASCADE)
    # site_meta = models.CharField(max_length=256)
    site_description = models.TextField(max_length=500)
    site_meta_tag =models.CharField(max_length=255)
    site_favicon = models.ImageField(upload_to='site_image/')
    site_logo = models.ImageField(upload_to='site_image/')
    slogan = models.CharField(max_length=150, default='')
    og_image = models.ImageField(upload_to='site_image/')
    mask_icon = models.FileField(upload_to='site_image/', validators=[FileExtensionValidator(['svg'])])    
    facebook_link = models.URLField()
    twitter_link = models.URLField()
    linkedin_link = models.URLField()    
    
    
    objects = models.Manager()
    on_site = CurrentSiteManager('site')
    
    def __str__(self):
        return self.site.__str__()  
    
    
class ResponseBackup(DateFieldModelMixin, models.Model):
    key = models.CharField(max_length=20,db_index=True)
    response = models.TextField()
    
    def __str__(self):
        return str(self.key) + str(self.id)
        
        
    
    
   

        
    
        
        
    
        
    
    

    
    
    

    