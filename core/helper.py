
from django.core.mail import get_connection
from django.apps import apps
from .models import Page, Blog, Category, ResponseBackup
from django.core.cache import cache
import openai
import os
from .models import (
    Category,
    Page,
    Blog
)
openai.api_key = os.getenv("OPENAI_API_KEY")   
def get_hwttp():
    res = cache.get('hwttp')
    if res is not None:
        return res
    res = ResponseBackup.objects.filter(key = 'howtotop')
    cache.set('hwttp', res, timeout=60 * 60)
    return res

def get_restext(sentence, title):
    if len(get_hwttp()) < 500:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'Please write a paraphrase of paragraph "{sentence}", which will encurage the blog reader to apply to the Job and give a positive vibh. Please keep the quoted name unchanged and please make sure that minimum response is 50 words.',
            temperature=0.82,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )           
        restext = str(response.choices[0].text)        
        ResponseBackup.objects.create(
            key = 'howtotop',
            response = restext
        )
        restext = restext.replace('XXXX', title)
    else:
        restext = sentence.replace('XXXX', title)
        
    return restext

def get_hwttb():
    res = cache.get('hwttb')
    if res is not None:
        return res
    res = ResponseBackup.objects.filter(key = 'howtobtm')
    cache.set('hwttb', res, timeout=60 * 60)
    return res

def get_restextb(sentence, title):
    if len(get_hwttb()) < 500:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'Please write a paraphrase of paragraph "{sentence}", which will encurage the blog reader to apply to the Job and give a positive vibh. Please keep the quoted name unchanged and please make sure that minimum response is 60 words.',
            temperature=0.82,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )           
        restext = str(response.choices[0].text)        
        ResponseBackup.objects.create(
            key = 'howtobtm',
            response = restext
        )
        restext = restext.replace('XXXX', title)
    else:
        restext = sentence.replace('XXXX', title)
        
    return restext

def get_blogs():
    # Check if the blogs are already in the cache
    blogs = cache.get('blogs')
    if blogs is not None:
        return blogs

    # If not in the cache, get the blogs from the database and store them in the cache
    blogs = Blog.published.all()
    cache.set('blogs', blogs, timeout=60 * 60)  # Set a timeout of 60 minutes (in seconds)
    return blogs

def categories():
    categories = cache.get('categories')
    if categories is not None:
        return categories
    categories = Category.objects.filter(is_active = True)
    cache.set('categories', categories, timeout=60 * 60)  # Set a timeout of 60 minutes (in seconds)
    return categories


def pages():
    pages = cache.get('pages')
    if pages is not None:
        return pages
    pages = Page.objects.filter(is_active = True) 
    cache.set('pages', pages, timeout=60 * 60)  # Set a timeout of 60 minutes (in seconds)
    return pages




COUNTRY_LIST = {
    
    'EU_COUNTRIES' : ['UK', 'DENMARK', 'POLAND', 'SWITHZERLAND', 'GERNAMY', 'NORWAY', 'SWEDEN', 'FINLAND'],
    'AMERICAN_COUNTRIES' : ['USA', 'CANADA', 'MEXICO', 'ARGENTINA', 'BRAZIL', 'AUSTRALIA'],
    'MIDDLEEAST_COUNTRIES' : ['UAE', 'SOUDIA ARABIA', 'QUATAR', 'ABUDABI'],
    'ASIAN_COUNTRIES' : ['INDIA', 'JAPAN', 'CHINA', 'PAKISTHAN', 'BANGLADESH', 'MALYESIA', 'SINGAPUR'],
    'OCENIA_COUNTRIES' : ['AUSTRALIA', 'NEWZELAND'],
    'AFRICAN_COUNTRIES' : ['ANGOLA', 'SOUTHAFRICA', 'ZIMBABWA', 'ZAMBIA']
        
}


JOB_POST = [
    'RETAILS SALES ASSOCIATE',
    'CUSTOMER SERVICE REPRESENTATIVE',
    'ASSISTANT MANAGER',
    'DEPARTMENT MANAGER',
    'STORE MANAGE',
    'LOGISTIC CO ORDINATOR',
    'SUPLY CHAIN ANALYST',
    'PRODUCT DEVELOPMENT MANAGER'
    ]
SALARY_RANGE_BLOCK = [
    '200000',
    '120000',
    '400000',
    '500000',
    '560000',
    '789541',
]

EXTRA_BLOCK_LIST = {
    'JOB_POST' : JOB_POST,
    'SALARY_RANGE_BLOCK' : SALARY_RANGE_BLOCK
}


def model_with_field(field_name):    
    models_with_field_name = []
    # Iterate over all installed apps
    for app_config in apps.get_app_configs():
        # Get all models for the current app
        for model in app_config.get_models():
            # Check if the model has a field named 'field_name'
            if hasattr(model, field_name):
                models_with_field_name.append(model)
    return models_with_field_name

# Imported for backwards compatibility and for the sake
# of a cleaner namespace. These symbols used to be in
# django/core/mail.py before the introduction of email
# backends and the subsequent reorganization (See #10355)
from django.core.mail.message import (
    
    EmailMultiAlternatives,
    EmailMessage,

)

def custom_send_mail(
    subject,
    message,
    from_email,
    recipient_list,
    fail_silently=False,
    auth_user=None,
    auth_password=None,
    connection=None,
    html_message=None,
    cc=None,
    reply_to=None,
    bcc=None,
):
    """
    Easy wrapper for sending a single message to a recipient list. All members
    of the recipient list will see the other recipients in the 'To' field.

    If from_email is None, use the DEFAULT_FROM_EMAIL setting.
    If auth_user is None, use the EMAIL_HOST_USER setting.
    If auth_password is None, use the EMAIL_HOST_PASSWORD setting.

    Note: The API for this method is frozen. New code wanting to extend the
    functionality should use the EmailMessage class directly.
    """
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    mail = EmailMultiAlternatives(
        subject, message, from_email, recipient_list, cc=cc, reply_to = reply_to, bcc=bcc, connection=connection
    )
    if html_message:
        mail.attach_alternative(html_message, "text/html")

    return mail.send()

def custom_send_mass_mail(
    datatuple, fail_silently=False, auth_user=None, auth_password=None, connection=None
):
    """
    Given a datatuple of (subject, message, from_email, recipient_list), send
    each message to each recipient list. Return the number of emails sent.

    If from_email is None, use the DEFAULT_FROM_EMAIL setting.
    If auth_user and auth_password are set, use them to log in.
    If auth_user is None, use the EMAIL_HOST_USER setting.
    If auth_password is None, use the EMAIL_HOST_PASSWORD setting.

    Note: The API for this method is frozen. New code wanting to extend the
    functionality should use the EmailMessage class directly.
    """
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    messages = [
        EmailMessage(subject, message, sender, recipient, cc=cc, reply_to=reply_to, bcc=bcc, connection=connection)
        for subject, message, sender, recipient, cc, reply_to, bcc in datatuple
    ]
    return connection.send_messages(messages)

