from pprint import pprint
import time
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
import openai
import os
from .models import *
from django.forms import formset_factory
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from createblog.forms import (
    NicheSelectionForm,
    OutlineForm,
    DraftForm,
    AddTopicForm
    ) 
openai.api_key = os.getenv("OPENAI_API_KEY")   

LABEL_FOR_NICHE = 'Please suggest 5 blog topics on niche'
LABEL_FOR_KEYWORDS = 'by considering keywords'
LABEL_FOR_NICHE_AREA = 'for'

@login_required
def createblog_home(request):
    if not request.user.is_superuser:
        raise Http404
    
    template_name = 'createblog/home.html'   

    niche_form = NicheSelectionForm()
    niche_form.fields['selected_niche'].label = LABEL_FOR_NICHE
    niche_form.fields['keywords'].label = LABEL_FOR_KEYWORDS
    niche_form.fields['niche_area'].label = LABEL_FOR_NICHE_AREA
    
    
    context = {
        'niche_form' : niche_form        
    }
    
    return render(request, template_name, context=context)

@login_required
def get_topics(request):
    if not request.user.is_superuser:
        return HttpResponse('You are not super user')    
    
    topics = Topic.objects.all()
    
    if request.method == 'POST':
        add_topic_form = AddTopicForm()
        
        niche_form = NicheSelectionForm(request.POST)     
           
        if niche_form.is_valid():
            niche_title = niche_form.cleaned_data['selected_niche']   
            keywords = niche_form.cleaned_data['keywords']               
            niche_area =  niche_form.cleaned_data['niche_area']           
        else:
            return HttpResponse(niche_form.errors)
        
        existing_topics = topics.filter(category_title = niche_title)
        completed_topics, incomplete_topic = get_processed_topic(request, existing_topics)
        
        if incomplete_topic.exists():
            return render(
                request, 
                'createblog/topic_list.html', 
                context={
                    'incomplete_topic': incomplete_topic, 
                    'completed_topics': completed_topics, 
                    'add_topic_form': add_topic_form,
                    'niche_title' : niche_title,
                    }
                )
        
        # existing_topics = topics.filter(category_title = niche_title)[:60]
        topic_titles = existing_topics.values_list('title', flat=True)
 
        joined_titles = "\n".join(topic_titles)
        
        max_token_limit = 4096  # Adjust this value based on the model's token limit
        if len(joined_titles) > max_token_limit:
            joined_titles = joined_titles[-max_token_limit:]
        
        prompt_body =  f"{LABEL_FOR_NICHE} : '{niche_title}' {LABEL_FOR_KEYWORDS} {keywords} {LABEL_FOR_NICHE_AREA} {niche_area}. Response topics only without any formal or extra text."  
        prompt = [
            {'role': 'system', 'content': 'You are creating Blog Topics'},            
            {'role': 'assistant', 'content': joined_titles },            
            {'role': 'user', 'content': prompt_body  , 'name': request.user.username}
        ]        
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,   
            temperature=1.2,         
            )
        
        # # Extract the generated outline from the response
        generated_outline = response.choices[0].message.content.split('\n')
        topic_objects = [Topic(category_title=niche_title, title=title) for title in generated_outline]
        Topic.objects.bulk_create(topic_objects)
        
        topics = Topic.objects.filter(category_title = niche_title)
        completed_topics, incomplete_topic = get_processed_topic(request, topics)
        
        return render(
            request, 
            'createblog/topic_list.html', 
            context={
                'incomplete_topic': incomplete_topic, 
                'completed_topics': completed_topics, 
                'add_topic_form': add_topic_form,
                'niche_title' : niche_title,
                }
            )
    
    return HttpResponse('Nothing to response')


@login_required
def delete_topic(request):  
    if not request.user.is_superuser:
        return HttpResponse('You are not super user')   
    if request.method == 'POST':     
        add_topic_form = AddTopicForm()
        topic = Topic.objects.get(id = int(request.POST.get('topic_id')))
        niche_title = topic.category_title       
        topics = Topic.objects.filter(category_title = niche_title)
        completed_topics, incomplete_topic = get_processed_topic(request, topics)
        topic.delete()
        return render(
            request, 
            'createblog/topic_list.html', 
            context={
                'incomplete_topic': incomplete_topic, 
                'completed_topics': completed_topics, 
                'add_topic_form': add_topic_form
                }
            )
    return HttpResponse('Nothing to response')
@login_required
def add_topic(request):
    if not request.user.is_superuser:
        return HttpResponse('You are not super user')  
    if request.method == 'POST':     
        add_topic_form = AddTopicForm(request.POST)
        
        if add_topic_form.is_valid():
            niche_title = add_topic_form.cleaned_data['selected_niche']   
            topic_title = add_topic_form.cleaned_data['topic']     
            Topic.objects.create(category_title = niche_title, title = topic_title)
        else:
            return HttpResponse(add_topic_form.errors)
        
        
        add_topic_form = AddTopicForm()
        topics = Topic.objects.filter(category_title = niche_title)
        
        completed_topics, incomplete_topic = get_processed_topic(request, topics)
        
        
        return render(
            request, 
            'createblog/topic_list.html', 
            context={
                'incomplete_topic': incomplete_topic, 
                'completed_topics': completed_topics, 
                'add_topic_form': add_topic_form
                }
            )
    return HttpResponse('Nothing to response')

@login_required
def get_processed_topic(request, topics):    
    completed_topics = topics.filter(completed = True)        
    incomplete_topic = topics.filter(completed = False)          
    # paginator = Paginator(completed_topics, 100) 
    # page_number = request.GET.get('page')
    # try:
    #     completed_topics = paginator.page(page_number)
    # except PageNotAnInteger:
    #     completed_topics = paginator.page(1)
    # except EmptyPage:
    #     completed_topics = paginator.page(paginator.num_pages)    
        
    return completed_topics, incomplete_topic
    
        

    
    

def get_outline(request):
    if not request.user.is_superuser:
        return HttpResponse('You are not super user')  
    OutlineFormSet = formset_factory(OutlineForm, extra=0)
    if request.method == 'POST':     
        topic_id = request.POST.get('topic_id')   
        if not  topic_id:
            messages.error(request, 'Topic not selected.')
            return redirect(reverse('createblog:get_topics'))
            
        topic = Topic.objects.get(id = int(topic_id))        
        topic_title = topic.title         
        
        if 'regenarate' in request.POST: 
            DraftBlog.objects.filter(topic = topic).delete()     
            Outline.objects.filter(topic = topic).delete()
                 
        existing_outline = Outline.objects.filter(topic = topic)           
        if existing_outline.exists():    
            formset = OutlineFormSet(initial=[{'outline': o.outline, 'id': o.id} for o in existing_outline])
            return render(request, 'createblog/outline.html', {'formset': formset, 'topic_id': topic_id, 'topic_title': topic_title})              
            
        else:        
            prompt = [{'role': 'user', 'content':f"Generate an outline for blog post on the topic: {topic_title}", 'name': f"{request.user.username}"},]                
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=prompt,   
                temperature=1.2,         
                )
            
            # Extract the generated outline from the response
            generated_outline = response.choices[0].message.content     
            section_list =  generated_outline.split('\n\n') if '\n\n' in generated_outline else generated_outline.split('\n') 
            outline_objects = [Outline(topic=topic, outline=outline) for outline in section_list]
            Outline.objects.bulk_create(outline_objects)
            existing_outline = Outline.objects.filter(topic = topic)   
            formset = OutlineFormSet(initial=[{'outline': o.outline, 'id': o.id} for o in existing_outline])
            return render(request, 'createblog/outline.html', {'formset': formset, 'topic_id': topic_id,'topic_title': topic_title})
    return HttpResponse('Nothing to response')

def confirm_outline(request):
    if not request.user.is_superuser:
        return HttpResponse('You are not super user')      
    OutlineFormSet = formset_factory(OutlineForm, extra=0)
    if request.method == 'POST':      
        formset = OutlineFormSet(request.POST)
        id_list = []     
        if formset.is_valid():
            outlines_to_update = []
            for form in formset:
                outline = form.cleaned_data['outline']
                id = form.cleaned_data['id']
                id_list.append(int(id))             
                outlines_to_update.append(Outline(id=int(id), outline=outline))
            Outline.objects.bulk_update(outlines_to_update, ['outline'])
        else:
            HttpResponse(formset.errors)
    existing_outline = Outline.objects.filter(id__in = id_list)   
    topic = existing_outline.first().topic
    topic_id = topic.id
    topic_title = topic.title   
    
    formset = OutlineFormSet(initial=[{'outline': o.outline, 'id': o.id} for o in existing_outline])
    return render(request, 'createblog/outline.html', {'formset': formset, 'topic_id': topic_id, 'topic_title': topic_title})
    
    
    
def generate_response_for_outline(messages):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.9,       
    )
    return response['choices'][0]['message']

def create_blog(request):

    if not request.user.is_superuser:
        return HttpResponse('You are not a superuser')    
    
    OutlineFormSet = formset_factory(OutlineForm, extra=0)    

    
    if request.method == 'POST':     
        formset = OutlineFormSet(request.POST)
     
        topic_id = request.POST.get('topic_id')    
        topic = Topic.objects.get(id = int(topic_id))        
        topic_title = topic.title 
        
        existing_draft = DraftBlog.objects.filter(topic = topic)
       
        if existing_draft.exists():
            
            draft_formset = get_draft_formset(existing_draft, topic)
            
            return render(request, 'createblog/draft_blog.html', context = {'draft_formset' : draft_formset, 'topic': topic})           
     

        
        if formset.is_valid(): 
            sections = []
            for form in formset:
                outline = form.cleaned_data['outline']
                id = form.cleaned_data['id']  
                keywords = form.cleaned_data['keywords']                
                              
                section_object = {
                    'topic' : topic,
                    'outline_id' : id,
                    'outline' : outline,
                    'keywords' : keywords           
                                  
                    }
                sections.append(section_object)                   
            generated_responses = []

            # Initial system message
            messages = [{'role': 'system', 'content': 'You are writing my blog.'}]
            draft_objects = []
            try:
                count = 1
                for section in sections:                    
                    prompt = "Please write the blog content precisely and comprehensively for the following section of the outline. Focus on this section only as I will ask about the next sections separately.\n\n"
                    prompt += "For each section, please provide well-researched and original content, avoiding duplication from previous sections. Make sure the information is up-to-date, SEO optimized and relevant.\n\n"
                    prompt += "When writing the content, consider the following:\n"
                    prompt += "- Provide a clear and friendly explanation of the topic.\n"
                    prompt += "- Include any necessary data, tables, or lists to support your explanation.\n"
                    prompt += "- Ensure that the content is free of plagiarism by using your own words and properly attributing any sources used.\n\n"
                    prompt += f"Blog Topic: {topic_title}\n\n"
                    prompt += f"Section Outline: {section['outline']}\n\n"  
                    prompt += f"Please keep in mind that you are writing section {count} out of {len(sections)}, so please keep consistency with previous sections. \n\n"  
                    prompt += "Please provide subtitle for the content if needed.\n\n"
                    if section.get('keywords').strip():
                        prompt += f"Additionaly you may consider keywords: {section.get('keywords').strip()}.\n\n"                    
                    prompt += "Please write your content below for this section of outline of the blog:"

                    # User message for the current topic
                    messages.append({'role': 'user', 'content': prompt})
                    
                    # Generate assistant response
                    response = generate_response_for_outline(messages[-3:])
                    count += 1
                    assistant_message = response['content']
                
                    messages.append({'role': 'assistant', 'content': assistant_message})
                    
                
                    generated_responses.append(assistant_message)      
                    
                    draft_objects.append(DraftBlog(topic = topic, outline_id = section['outline_id'], response = assistant_message))
                            
                    time.sleep(5)
                 
            except Exception as e:
                return HttpResponse(f'Somethings error \n {e}')
            
                
            DraftBlog.objects.bulk_create(draft_objects)
            
            existing_draft = DraftBlog.objects.filter(topic = topic)       
            
            if existing_draft.exists():           
                draft_formset = get_draft_formset(existing_draft, topic)               
                return render(request, 'createblog/draft_blog.html', context = {'draft_formset' : draft_formset, 'topic': topic})    
            
    return HttpResponse('Nothing to response')

def get_draft_formset(existing_draft, topic):
    DraftFormSet = formset_factory(DraftForm, extra=0)
    draft_formset =  DraftFormSet(initial=[{'topic_id':d.topic.id, 'outline_id': d.outline_id, 'response': d.response.replace('\n', '<br>')} for d in existing_draft])            
    outline_ids = [form.initial.get('outline_id') for form in draft_formset]
    outline_data = dict(Outline.objects.filter(topic=topic, id__in=outline_ids).values_list('id', 'outline'))   
    for form in draft_formset:
        outline_id = form.initial.get('outline_id')
        outline_text = outline_data.get(outline_id)
        form.fields['response'].label = outline_text
    return draft_formset

def edit_draft(request):
    if not request.user.is_superuser:
        return HttpResponse('You are not a superuser')   
    DraftFormSet = formset_factory(DraftForm, extra=0)
    if request.method == 'POST':      
        draft_formset = DraftFormSet(request.POST)
        topicid = []
        if draft_formset.is_valid():             
            for form in draft_formset:    
                outline_id = form.cleaned_data['outline_id']
                topic_id = form.cleaned_data['topic_id']
                response = form.cleaned_data['response']
                topicid.append(topic_id)
                draft_blog = DraftBlog.objects.get(topic__id = topic_id, outline_id = outline_id)
                draft_blog.response = response
                draft_blog.save()           
        topic = Topic.objects.get(id = int(topicid[0]))
        existing_draft = DraftBlog.objects.filter(topic = topic)   
        draft_formset = get_draft_formset(existing_draft, topic)               
        return render(request, 'createblog/draft_blog.html', context = {'draft_formset' : draft_formset, 'topic': topic})       
    
    return HttpResponse('Nothing to response')

def draft_to_blog(request):
    from django.contrib.sites.shortcuts import get_current_site
    from core.models import Blog, Category
    
    if not request.user.is_superuser:
        return HttpResponse('You are not a superuser')  
    
    DraftFormSet = formset_factory(DraftForm, extra=0)
    if request.method == 'POST':      
        draft_formset = DraftFormSet(request.POST) 
        
    topic_id = set()
    section_list = []  
    if draft_formset.is_valid():             
        for form in draft_formset:   
            topicid = form.cleaned_data['topic_id']
            topic_id.add(topicid)
            response = form.cleaned_data['response']       
            section_list.append(response)   
    topic = Topic.objects.get(id = list(topic_id)[0])
    categories = Category.objects.filter(title = topic.category_title)
    body = ''.join(section_list) 
    blog = Blog(       
        title = topic.title,    
        creator = request.user,       
        ref_link = get_current_site(request).domain,
        body = body,
        status = 'draft',
        should_have_hta = False,
        should_have_apf = False,
        should_as_it_is = True
    )
    try:
        blog.save(request=request)  
    except:     
        messages.warning(request, 'Try to regenarate or contact with developper!')   
        return redirect(reverse('createblog:get_draft_blog', args=[int(topic.id)]))  
       
    blog.categories.add(*categories)    
    
    topic.completed=True
    topic.save()
    
    DraftBlog.objects.filter(topic = topic).delete()
    
    admin_url_path = f'/admin/{blog._meta.app_label}/{blog._meta.model_name}/{blog.id}/change/'    
    return render(request, 'createblog/draft_to_blog.html', context={'admin_url_path':admin_url_path})

def get_draft_blog(request, topic_id):
    
    if not request.user.is_superuser:
        return HttpResponse('You are not a superuser!')  
    
    topic = Topic.objects.get(id = topic_id)
    existing_draft = DraftBlog.objects.filter(topic = topic)   
    draft_formset = get_draft_formset(existing_draft, topic)  
    
    return render(request, 'createblog/draft_blog.html', context = {'draft_formset' : draft_formset, 'topic': topic})     
    
   

    
    
            
    
    
    