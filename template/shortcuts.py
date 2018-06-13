import os.path
from importlib import import_module
from core.handlers.wsgi import WSGIResponse
from template.html import HtmlTemplite

try:
    setting_path = os.environ.get('SETTING_MODULE')
    settings = import_module(setting_path)
except:
    pass

def render(request, template_name, context=None, context_type=None, status=None):
    """Returns an WSGIResponse object that had been compiled with the template and a context dictionary 

    [Keyword argument]:
    request --- the WSGIRequest object that passed from WSGIHandler
    template_name --- the template user wnat to compile and return
    context --- the dictionary value user wnat to combine with template
    context_type --- the type user want the content header is
    status --- response status

    [Return]:
    A WSGIResponse object which content is template compiled with context
    """
    template_name = get_template(template_name)
    if os.path.isfile(template_name) is False:
        pass
    else:
        if context_type is None:
            context_type = "text/html"
        content = HtmlTemplite(template_name).render(context)
        return WSGIResponse(content,context_type,status)

def get_template(template_name):
    """Get the complete path of the template
    
    [Keyword argument]
    template_name --- the template user wnat to compile and return

    [Return]
    the string which is compelte template path
    """
    base_dir = settings.BASE_DIR
    templates = settings.TEMPLATES

    for tpl in templates:
        for template_dir in tpl['DIRS']:

            # 目前views 不能render'/{html file}'
            template_path = os.path.join(base_dir,template_dir,template_name)
            
            if os.path.isfile(template_path):
                return template_path
    return None
