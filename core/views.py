from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import requests
from core.agent_helper import get_client_ip
from .models import Page, Blog, Action, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from .forms import CVForm
from .helper import (
    COUNTRY_LIST, 
    EXTRA_BLOCK_LIST,     
    categories,
    get_hwttp,
    get_restext,
    get_hwttb,
    get_restextb,
    get_blogs
    ) 

from .agent_helper import (
    get_para_list_from,
    get_hwt_block
)

# from django.db.models import Sum, Count, Q
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from core.context_processor import site_data
from django.utils.html import strip_tags

import logging
log =  logging.getLogger('log')


# Create your views here.
def home(request):
    template_name = 'core/home.html'
    blogs = get_blogs()
    
    paginator = Paginator(blogs, 10) 

    page_number = request.GET.get('page')
    try:
        blogs = paginator.page(page_number)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)          
  
        
    site = site_data()
    site['name'] = 'Ultimate Resource for International Job Seekers'
    
    context = {
        'blogs' : blogs,
        'site_data' : site
    }
    return render(request, template_name, context=context)


def category_detail(request, slug):
    template_name = 'core/category_details.html'
    
    category = get_object_or_404(Category, slug=slug)     
    blogs = category.blogs_category.filter(status = 'published')
    
    paginator = Paginator(blogs, 10) 

    page_number = request.GET.get('page')
    try:
        blogs = paginator.page(page_number)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages) 
        
        
    site = site_data()
    site['name'] = category.title[:40]
    truncated_string = strip_tags(category.description)[:160]
    site['description'] = truncated_string
    
     
    context = {
        'category' : category,
        'blogs': blogs,
        'site_data' : site
    }
    
    return render(request, template_name, context=context)


def page_detail(request, slug):
    template_name = 'core/page_detail.html'
    
    page = get_object_or_404(Page, slug=slug) 
    
    site = site_data()
    site['name'] = page.title[:40]
    
    
    context = {
        'page' : page,
        'site_data' : site
    }
    
    return render(request, template_name, context=context)   


    
def blog_detail(request, slug):
    template_name = 'core/blog_detail.html'
    
    blog = get_object_or_404(Blog.published, slug=slug)   
     
    blog.view(request)   
    
    '''
    OUTPUT STRING, PROCESSED OR AS IT IS BODY
    '''
    if not blog.should_as_it_is:
        
        # get list of pargraph by th help of beautifulsoup
        paragraphs = get_para_list_from(blog.body)   
      
        indicator_links = blog.latest_indicator_links_blocks(len(paragraphs))    
        table_links = blog.build_table_link_blocks(len(paragraphs))   
    
    
        
        output_list = []
        used_paragraphs = set()
        
        # Loop over each paragraph in the list of paragraphs, except the last one
        for i in range(len(paragraphs)-1):
            # Check if the current paragraph index is already used, if so skip it
            if i in used_paragraphs:
                continue

            # Add the current paragraph to the output list
            output_list.append(paragraphs[i])
            # Add the current paragraph index to the used_paragraphs set to mark it as used
            used_paragraphs.add(i)
            
            if i % 2 != 0:
                try:
                    # If there are indicator links for the current paragraph
                    if indicator_links[i]:
                        # Add a <div> tag to the output list
                        
                        # Loop over each indicator link for the current paragraph
                        for qs in indicator_links[i]:
                            # Add a bold text and a link to the output list
                            output_list.append('<div class="my-2">')
                            output_list.append(f'<b class="text-warning">CLick also <i class="fa-solid fa-hand-point-right"></i> </b><a class="link-success text-decoration-none text-capitalize" href="{qs.get_absolute_url()}">{qs.title}</a>')
                            output_list.append('</div>')
                        # Add a closing <div> tag to the output list
                        
                        output_list.append('<div>')
                        output_list.append('</div>')
                except:
                    blogs = get_blogs()[len(paragraphs):len(paragraphs) + 6]                
                    output_list.append('<div>')
                    # Add a <table> tag to the output list to start the table
                    output_list.append('<table class="table">')
                    # Loop over each table link for the current paragraph
                    for qs in blogs:
                        # Add a table row with two columns containing the title and 'UK' to the output list
                        if qs.extra_blocks == 'SALARY_RANGE_BLOCK':
                            output_list.append(
                                    '<tr class="text-uppercase"><td><a class="link-primary text-decoration-none" href="{}">{}</a></td><td><a class="link-primary text-decoration-none" href="{}">{}</a></td></tr>'
                                    .format(qs.get_absolute_url(), qs.title, qs.get_absolute_url(), random.choice(EXTRA_BLOCK_LIST.get(qs.extra_blocks)))
                                    ) 
                        if qs.extra_blocks == 'JOB_POST':
                            output_list.append(
                                    '<tr class="text-uppercase"><td><a class="link-primary text-decoration-none" href="{}">{}</a></td></tr>'
                                    .format(qs.get_absolute_url(), random.choice(EXTRA_BLOCK_LIST.get(qs.extra_blocks)))
                                    )                         
                    # Add a closing </table> tag to the output list to end the table
                    output_list.append('</table>')
                    output_list.append('</div>')                
                    output_list.append('<div>')
                    output_list.append('</div>')

                # Check if the next paragraph index is already used, if so skip it
                if i+1 in used_paragraphs:
                    continue
                        
                # Try to add the next paragraph to the output list
                try:
                    output_list.append(paragraphs[i+1])
                    # Add the next paragraph index to the used_paragraphs set to mark it as used
                    used_paragraphs.add(i+1)
                    
                    # If there are table links for the current paragraph
                    if table_links:
                        # Add a <table> tag to the output list to start the table
                        output_list.append('<div>')
                        output_list.append('<table class="table">')
                        # Loop over each table link for the current paragraph
                        for qs in table_links[i]:
                            # Add a table row with two columns containing the title and 'UK' to the output list
                            output_list.append(
                                '<tr class="text-uppercase"><td><a class="link-primary text-decoration-none" href="{}">{}</a></td><td><a class="link-primary text-decoration-none" href="{}">{}</a></td></tr>'
                                .format(qs.get_absolute_url(), qs.title, qs.get_absolute_url(), random.choice(COUNTRY_LIST.get(qs.job_area)))
                                ) 
                        # Add a closing </table> tag to the output list to end the table
                        output_list.append('</table>')
                        output_list.append('</div>')
                        output_list.append('<div>')
                        output_list.append('</div>')
                except:
                    blogs = get_blogs()[len(paragraphs) + 6:len(paragraphs) + 12]                
                    output_list.append('<div>')
                    # Add a <table> tag to the output list to start the table
                    output_list.append('<table class="table">')
                    # Loop over each table link for the current paragraph
                    for qs in blogs:
                        # Add a table row with two columns containing the title and 'UK' to the output list
                        if qs.extra_blocks == 'SALARY_RANGE_BLOCK':
                            output_list.append(
                                    '<tr class="text-uppercase"><td><a class="link-primary text-decoration-none" href="{}">{}</a></td><td><a class="link-primary text-decoration-none" href="{}">{}</a></td></tr>'
                                    .format(qs.get_absolute_url(), qs.title, qs.get_absolute_url(), random.choice(EXTRA_BLOCK_LIST.get(qs.extra_blocks)))
                                    ) 
                        if qs.extra_blocks == 'JOB_POST':
                            output_list.append(
                                    '<tr class="text-uppercase"><td><a class="link-primary text-decoration-none" href="{}">{}</a></td></tr>'
                                    .format(qs.get_absolute_url(), random.choice(EXTRA_BLOCK_LIST.get(qs.extra_blocks)))
                                    )                         
                    # Add a closing </table> tag to the output list to end the table
                    output_list.append('</table>')
                    output_list.append('</div>')                
                    output_list.append('<div>')
                    output_list.append('</div>')
            
            
            
        
        output_string = ''.join(output_list)
    else:
        output_string = blog.body
        
    '''
    APPLICATION FORM
    '''
    if blog.should_have_apf:      
        form = CVForm()       
    else:
        form = None
        
        
    
    
    
    if not blog.should_as_it_is:
        blog.title = f'{blog.title} {", ".join(COUNTRY_LIST.get(blog.job_area))}'
        
    site = site_data()
    site['name'] = blog.title[:45]
    truncated_string = strip_tags(blog.body)[:160]
    site['description'] = truncated_string
    site['og_image'] = blog.feature.url
    
    
    context = {
        'output_string' : output_string,
        'blog' : blog,
        'form' : form,       
        'site_data' : site
       
    }   
    
    return render(request, template_name, context=context)

def hta(request, slug):
    template_name = 'core/hta.html'   
    blog = get_object_or_404(Blog.published, slug=slug)   
    # get How to block with the help of OpenAI  
    how_to_block = get_hwt_block(blog)   
    output_string = ''.join(how_to_block)
    
    context = {
        'hta' : output_string    
    }  
    
    return render(request, template_name, context=context)
    
    

def like_or_dislike(request, content_type_id, object_id):
    request_action = request.GET.get('action')
    if request_action not in ('like', 'dislike'):
        log.error(f"Template configuration error in {request.path}, should have 'like' or 'dislike' in <blog.like_or_dislike_url|add_action:'like'> formate!")
        messages.error(request, 'Can not complete the operation for internal error.')
        return HttpResponse('Can not complete the operation for internal error.')    
    content_type = ContentType.objects.get(id = content_type_id)   
    # Get the model class
    model_class = content_type.model_class()
    # Get the model object
    model_object = model_class.objects.get(id=object_id)
    
    
    if request_action == 'like':
    
        Action.objects.create(
            content_type=content_type,
            object_id=object_id,
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
            action_type=Action.LIKE
        )
    if request_action == 'dislike':    

        Action.objects.filter(
            content_type=content_type,
            object_id=object_id,
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
            action_type=Action.LIKE
        ).delete()
        
   
    
    template_name = 'htmx/like_or_dislike.html'
    
    context = {  
        'blog' : model_object
    }
    
    return render(request, template_name, context=context)


def success(request):     
    if request.method == 'POST':
        form = CVForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:   
            errors = '\n'.join([f"{field}: {error}" for field, error in form.errors.items()])
            return HttpResponse(f'Form errors:\n{errors}')            
        return HttpResponse('Application Submitted successfully')
    
    

    





