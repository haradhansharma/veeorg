from django import template
from core.agent_helper import get_client_ip
from core.helper import COUNTRY_LIST
from core.models import Action




register = template.Library()



@register.filter
def get_country_list(value):
    list = COUNTRY_LIST[value]
    return ', '.join(list)

@register.filter
def add_action(url, action):
    return f'{url}?action={action}'
    
    
    
@register.filter
def is_liked_by_user_or_ip(value, request):   
    actions = Action.objects.select_related('user').filter(content_type=value.get_content_type, action_type=Action.LIKE, object_id = value.id)
    if request.user.is_authenticated:
        actions = actions.filter(user=request.user)
    else:
        actions = actions.filter(ip_address=get_client_ip(request)) 
    return actions.exists()




