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
    """Summary

    [Keyword argument]:
    request --

    [Return]:
    A WSGIResponse object

    [Description]
    Return a WSGIResponse whose content is filled with html file content that is compiled by template engine
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
    """Summary

    [Keyword argument]

    [Return]
    A HtmlTemplite object

    [Description]

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
