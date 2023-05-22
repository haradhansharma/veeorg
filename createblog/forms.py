from django import forms
from core.helper import categories
from django_summernote.widgets import SummernoteWidget
import bleach
from django_summernote.settings import ALLOWED_TAGS, ATTRIBUTES, STYLES
from django.forms import fields




class CustomSummernoteTextFormField(fields.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.update({'widget': SummernoteWidget()})
        super().__init__(*args, **kwargs)
    def to_python(self, value):
        value = super().to_python(value)
        return bleach.clean(
            value, tags=ALLOWED_TAGS, attributes=ATTRIBUTES, css_sanitizer=STYLES)
    


class NicheSelectionForm(forms.Form):
    category_choices = categories().values_list('title', 'title')
    selected_niche = forms.ChoiceField(choices=category_choices, widget=forms.Select(attrs={'class': 'form-select'}))
    extra_text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
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
    
    
    