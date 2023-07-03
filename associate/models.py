from django.db import models
from django.utils.translation import activate, gettext_lazy as _

from core.mixins import (
    TitleAndSlugModelMixin, 
    CreatorModelMixin,    
    SitesModelMixin,
    IsActiveModelMixin,
    MenuModelMixin,
    SaveFromAdminMixin,
    DateFieldModelMixin,
    ) 

class AssociateAt(
    TitleAndSlugModelMixin, 
    CreatorModelMixin,    
    SitesModelMixin,
    IsActiveModelMixin,
    MenuModelMixin,
    DateFieldModelMixin,
    models.Model
    ): 
         
    public_url = models.URLField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Associate At')
        verbose_name_plural = _('All Associates')    
        ordering = ['-created_at'] 
    
