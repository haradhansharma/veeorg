
from django.urls import path, include
from .views import *
from django.views.generic.base import TemplateView


app_name = 'createblog'



urlpatterns = [
    
    path('createblog-home/', createblog_home, name='createblog_home'),
    path('get-topics/', get_topics, name='get_topics'),
    path('get-outline/', get_outline, name='get_outline'),
    path('confirm-outline/', confirm_outline, name='confirm_outline'),
    path('create-blog/', create_blog, name='create_blog'),
    path('edit-draft/', edit_draft, name='edit_draft'),
    path('delete-topic/', delete_topic, name='delete_topic'),
    path('add-topic/', add_topic, name='add_topic'),
    path('draft-to-blog/', draft_to_blog, name='draft_to_blog'),
    path('get-draft-blog/<int:topic_id>', get_draft_blog, name='get_draft_blog'),
    
    
    
    
    
    
    
    
    

    
    
    
]
