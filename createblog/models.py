from django.db import models

class Topic(models.Model):
    category_title = models.CharField(max_length=252)
    title = models.TextField()
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics' 
        ordering = ['-id'] 
        
class Outline(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    outline = models.TextField()
    
    def __str__(self):
        return self.outline
    
    class Meta:
        verbose_name = 'Outline'
        verbose_name_plural = 'Outlines' 
        ordering = ['id'] 
        
class DraftBlog(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    outline_id = models.BigIntegerField()
    response = models.TextField()
    
    @property
    def outline(self):
        return Outline.objects.get(id = self.outline_id)
    
    def __str__(self):
        return self.topic.title
    
    class Meta:
        verbose_name = 'Draft Blog'
        verbose_name_plural = 'Draft Blogs' 
        ordering = ['id'] 
    
    


