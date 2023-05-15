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