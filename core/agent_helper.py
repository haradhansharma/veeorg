from bs4 import BeautifulSoup
import random

#helper functions
def get_client_ip(request):
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:        
        ip = x_forwarded_for.split(',')[-1].strip()    
    elif request.META.get('HTTP_CLIENT_IP'):        
        ip = request.META.get('HTTP_CLIENT_IP')
    elif request.META.get('HTTP_X_REAL_IP'):        
        ip = request.META.get('HTTP_X_REAL_IP')
    elif request.META.get('HTTP_X_FORWARDED'):        
        ip = request.META.get('HTTP_X_FORWARDED')
    elif request.META.get('HTTP_X_CLUSTER_CLIENT_IP'):        
        ip = request.META.get('HTTP_X_CLUSTER_CLIENT_IP')
    elif request.META.get('HTTP_FORWARDED_FOR'):        
        ip = request.META.get('HTTP_FORWARDED_FOR')
    elif request.META.get('HTTP_FORWARDED'):        
        ip = request.META.get('HTTP_FORWARDED')
    elif request.META.get('HTTP_VIA'):        
        ip = request.META.get('HTTP_VIA')    
    else:        
        ip = request.META.get('REMOTE_ADDR')
        
    return ip

#helper function
def get_agent(request):   
    
    results = {}        
    if request.user_agent.is_mobile:
        user_usage = 'Mobile'        
    elif request.user_agent.is_tablet:
        user_usage = 'Tablet'    
    elif request.user_agent.is_touch_capable:
        user_usage = 'Touch Capable'
    elif request.user_agent.is_pc :
        user_usage = 'PC'
    elif request.user_agent.is_bot :
        user_usage = 'BOT'
    else:
        user_usage = 'Not able to figur out'        
    
    data = {
        'user_usage' : user_usage ,
        'user_browser' : request.user_agent.browser,
        'user_os' : request.user_agent.os ,
        'user_device' : request.user_agent.device          
    }    
    results.update(data)
    
    
    return results


def get_para_list_from(html):
    soup = BeautifulSoup(html, 'html.parser')       
    # use a set for faster membership testing
    valid_parent_tags = {'p', 'img', 'span', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'codeblock', 'ul', 'ol', 'li', 'a', 'blockquote', 'figure'}
    paragraphs = []
    for tag in soup.find_all(valid_parent_tags):
        if tag.name == 'img':
            # get the parent of the img tag and append both
            parent_tag = tag.parent
            paragraphs.append(str(parent_tag))            
        else:
            # use stripped_strings to get all non-empty strings inside the tag
            text = ''.join(tag.stripped_strings)
            if text:
                if tag.parent.name in valid_parent_tags:
                    continue
                paragraphs.append(str(tag))
    
    return paragraphs

def get_hwt_block(blog):
    from .helper import (    
    get_hwttp,
    get_restext,
    get_hwttb,
    get_restextb  
    ) 
    
    
    output_list = []
    output_list.append('<h2>')
    output_list.append(f'How to Apply for {blog.title} ?')
    output_list.append('</h2>')   
    
    #top text of how to apply block by the help of openAI
    sentence = random.choice(get_hwttp())         
    restext = get_restext(sentence.response, blog.title)
    
    output_list.append('<p>')
    output_list.append(restext)
    output_list.append('</p>')   
    
    output_list.append('<p>')
    output_list.append(f'Here are the steps to follow when applying for a job at {blog.title}:')
    output_list.append('</p>')  
    
    
    output_list.append('<ol>')
    output_list.append(f'<li>Click on the <a class="link-success text-decoration-none" target="_blank" href="{blog.ref_link}">Careers</a> or <a class="link-success text-decoration-none" target="_blank" href="{blog.ref_link}">Join Our Team</a> link on the {blog.title} job page to view all available job openings.</li>')
    output_list.append('<li>Review the job descriptions carefully to ensure that you meet the qualifications and requirements for the position.</li>')
    output_list.append(f"<li>Click on the <a class='link-success text-decoration-none' target='_blank' href='{blog.ref_link}'>Apply</a> button for the position you're interested in to begin the application process.</li>")
    output_list.append('<li>Fill out the online application form with your personal and professional information, including your resume and cover letter.</li>')
    output_list.append('<li>If required, complete any additional assessments or questionnaires related to the position.</li>')
    output_list.append('<li>Double-check your application for accuracy and completeness before submitting it.</li>')   
    output_list.append('</ol>')  
    
    #Bottom text of how to apply block by the help of openAI
    sentenceb = random.choice(get_hwttb())         
    restextb = get_restextb(sentenceb.response, blog.title.capitalize())
    
    
    output_list.append('<p>')
    output_list.append(restextb)
    output_list.append('</p>')  
    
    return output_list