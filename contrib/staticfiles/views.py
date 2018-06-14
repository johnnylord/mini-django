import os
from importlib import import_module
from core.handlers.wsgi import WSGIResponse

try:
    setting_path = os.environ.get('SETTING_MODULE')
    settings = import_module(setting_path)
except:
    pass

def serve_static(request, staticfile):
    """process static request and return a response with static file content

    [Keyword arguments]:
    request --- request from browser
    staticfile --- the path to static file

    [Return]:
    WSGIResponse object
    """
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
    """via static file and BASE_DIR and STATIC_URL in settings to get compelete path to static file
    
    [Keyword arguments]:
    staticfile --- the path to static file

    [Return]:
    None or a complete path to static file
    """

    base_dir = settings.BASE_DIR
    static_url = "static/"
    installed_apps = settings.INSTALLED_APPS

    for app in installed_apps:
        static_path = os.path.join(base_dir,app,static_url,staticfile)
        if os.path.isfile(static_path):
            return static_path
    return None

def _get_content_type(static_path):
    """via file type to determine the content type of response

    [Keyword arguments]:
    static_path --- compelete path to static file

    [Return]:
    a string which indicate the content type of response
    """

    content_type=None
    static_path = static_path.split('.')
    
    if static_path[1].startswith("css"):
        content_type = 'text/css'
    elif static_path[1].startswith("js") or static_path[1].startswith("javascript"):
        content_type = "text/javascript"
    return content_type
