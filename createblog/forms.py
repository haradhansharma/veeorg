from django import forms
from core.helper import categories
from django_summernote.widgets import SummernoteWidget
import bleach
from django_summernote.settings import ALLOWED_TAGS, ATTRIBUTES, STYLES
from django.forms import fields

from core.models import Category




class CustomSummernoteTextFormField(fields.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.update({'widget': SummernoteWidget()})
        super().__init__(*args, **kwargs)
    def to_python(self, value):
        value = super().to_python(value)
        return bleach.clean(
            value, tags=ALLOWED_TAGS, attributes=ATTRIBUTES, css_sanitizer=None)
        
    
class AddTopicForm(forms.Form):
    category_choices = Category.objects.all().values_list('title', 'title')
    selected_niche = forms.ChoiceField(label='Select Niche',choices=category_choices, widget=forms.Select(attrs={'class': 'form-select'}))
    topic = forms.CharField(label='Write title of the topic you want to add', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write full Topic'}))
    
    
    


class NicheSelectionForm(forms.Form):
    category_choices = Category.objects.all().values_list('title', 'title')
    selected_niche = forms.ChoiceField(choices=category_choices, widget=forms.Select(attrs={'class': 'form-select'}))
    keywords = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma separated keywords here. e.g: dreams, bitcoin etc.'}))
    niche_area = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Niche area here, e.g. internation job market, International Business etc'}))

    
class OutlineForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())    
    outline = forms.CharField(label='', widget=forms.Textarea(attrs={'class':'form-control', 'rows':3}))
    keywords = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'You may write some keywords here, but it will not saved.'}))
    
    
class DraftForm(forms.Form):
    topic_id = forms.IntegerField(widget=forms.HiddenInput())
    outline_id = forms.IntegerField(widget=forms.HiddenInput())
    response = CustomSummernoteTextFormField()
    
    
    # def __init__(self, *args, **kwargs):
    #     response_label = kwargs.pop('response_label', None)
    #     super(DraftForm, self).__init__(*args, **kwargs)
        
    #     if response_label:
    #         self.fields['response'].label = response_label
    
    
    