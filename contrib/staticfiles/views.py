import os
from importlib import import_module
from core.handlers.wsgi import WSGIResponse

try:
    setting_path = os.environ.get('SETTING_MODULE')
    settings = import_module(setting_path)
except:
    pass

def serve_static(request, staticfile):
    static_path = _get_static(staticfile)
    static_content = None
    content_type = _get_content_type(static_path)

    try:
    # Get the content of html text file
        with open(static_path, 'r') as fin:
            static_content = fin.read()
    except:
        raise
    return WSGIResponse(static_content, content_type=content_type)
        

def _get_static(staticfile):
    base_dir = settings.BASE_DIR
    static_url = "static/"
    installed_apps = settings.INSTALLED_APPS

    for app in installed_apps:
        static_path = os.path.join(base_dir,app,static_url,staticfile)
        if os.path.isfile(static_path):
            return static_path
    return None

def _get_content_type(static_path):
    content_type=None
    static_path = static_path.split('.')
    
    if static_path[1].startswith("css"):
        content_type = 'text/css'
    elif static_path[1].startswith("js") or static_path[1].startswith("javascript"):
        content_type = "text/javascript"
    return content_type
