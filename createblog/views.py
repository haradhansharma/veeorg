from pprint import pprint
import time
from django.http import Http404, HttpResponse
from django.shortcuts import render
import openai
import os
from .models import *
from django.forms import formset_factory
from createblog.forms import (
    NicheSelectionForm,
    OutlineForm,
    DraftForm
    # TopicForm
    ) 
openai.api_key = os.getenv("OPENAI_API_KEY")   


def createblog_home(request):
    if not request.user.is_superuser:
        raise Http404
    
    template_name = 'createblog/home.html'    
    
    # if request.method == 'POST':
        # topic_form = TopicForm(request.POST)        
        # if topic_form.is_valid():
        #     topic = topic_form.cleaned_data['topic']
        # else:
        #     return HttpResponse(topic_form.errors)
            
        # prompt = [{'role': 'user', 'content':f"Generate an outline for a blog post on the topic: {topic}", 'name': f"{request.user.username}"},]        
        
        
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=prompt,   
        #     temperature=1.2,         
        #     )
        
        # # Extract the generated outline from the response
        # generated_outline = response.choices[0].message.content        
        
        # # Pass the generated outline to the template for rendering
        # return render(request, 'createblog/outline.html', {'outline': generated_outline})
    
    # topic_form = TopicForm()
    niche_form = NicheSelectionForm()
    
    context = {
        # 'topic_form' : topic_form,
        'niche_form' : niche_form        
    }
    
    return render(request, template_name, context=context)


def get_topics(request):
    if not request.user.is_superuser:
        return HttpResponse('You are not super user')    
    if request.method == 'POST':
        niche_form = NicheSelectionForm(request.POST)        
        if niche_form.is_valid():
            niche_title = niche_form.cleaned_data['selected_niche']   
            extra_text =  niche_form.cleaned_data['extra_text']           
        else:
            return HttpResponse(niche_form.errors)
        incomplete_topic = Topic.objects.filter(category_title = niche_title, completed = False)[:60]
        if incomplete_topic.exists():
            return render(request, 'createblog/topic_list.html', context={'incomplete_topic': incomplete_topic})
        
        existing_topics = Topic.objects.filter(category_title = niche_title)[:60]
        topic_titles = existing_topics.values_list('title', flat=True)
        joined_titles = "\n".join(topic_titles)
        
        max_token_limit = 4096  # Adjust this value based on the model's token limit
        if len(joined_titles) > max_token_limit:
            joined_titles = joined_titles[:max_token_limit]
            
        prompt = [
            {'role': 'system', 'content': joined_titles},
            {'role': 'user', 'content': f"Suggest some topics of blog post based on : '{niche_title}' {extra_text}" , 'name': request.user.username}
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
        incomplete_topic = Topic.objects.filter(category_title = niche_title, completed = False)[:60]
        return render(request, 'createblog/topic_list.html', context={'incomplete_topic': incomplete_topic})
    return HttpResponse('Nothing to response')

def get_outline(request):
    if not request.user.is_superuser:
        return HttpResponse('You are not super user')  
    OutlineFormSet = formset_factory(OutlineForm, extra=0)
    if request.method == 'POST':     
        topic_id = request.POST.get('topic_id')    
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
    topic = existing_outline.first()
    topic_id = topic.topic_id
    topic_title = topic.topic_title
    
    
    formset = OutlineFormSet(initial=[{'outline': o.outline, 'id': o.id} for o in existing_outline])
    return render(request, 'createblog/outline.html', {'formset': formset, 'topic_id': topic_id, 'topic_title': topic_title})
    
    
    
def generate_response_for_outline(messages):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.8,
       
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
                    prompt += f"Please keep in mind that you are writing section {count} out of {len(sections)}. \n\n"  
                    prompt += "Please provide subtitle for the content if needed.\n\n"
                    if section.get('keywords').strip():
                        prompt += f"Additionaly you may consider keywords: {section.get('keywords').strip()}.\n\n"                    
                    prompt += "Please write your content for this section of outline of the blog below:"

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
                    # Clear the user and assistant messages for the next iteration
                    # messages = messages[:1]
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
    
    
            
    
    
    