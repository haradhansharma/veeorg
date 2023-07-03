from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import requests
from core.agent_helper import get_client_ip
# from .models import Page, Blog, Action, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from core.helper import (
    COUNTRY_LIST, 
    EXTRA_BLOCK_LIST,     
    categories,
    get_hwttp,
    get_restext,
    get_hwttb,
    get_restextb,
    get_blogs
    ) 

from core.agent_helper import (
    get_para_list_from,
    get_hwt_block
)

from django.db.models import Sum, Count, Q
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from core.context_processor import site_data
from django.utils.html import strip_tags

import logging
log =  logging.getLogger('log')


def picked_essentials(request):
    template_name = 'associate/picked_essentials.html'
    
    context = {
        'blogs' : 'blogs',
        'site_data' : 'site'
    }
    return render(request, template_name, context=context)
