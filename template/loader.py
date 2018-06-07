# from template.html import HtmlTemplite
from importlib import import_module
import os

setting_path = os.environ.get('SETTING_MODULE')
settings = import_module(setting_path)


def get_template(template_name):

    base_dir = settings.BASE_DIR
    templates = settings.TEMPLATES

    for tpl in templates:
        for template_dir in tpl['DIRS']:

            # 目前views 不能render'/{html file}'
            template_path = os.path.join(base_dir,template_dir,template_name)
            
            if os.path.isfile(template_path):
                return template_path
    return None


def get_static(static_name):

    base_dir = settings.BASE_DIR
    static_url = settings.STATIC_URL
    installed_apps = settings.INSTALLED_APPS

    for app in installed_apps:
        static_path = os.path.join(base_dir,app,static_url,static_name)

        if os.path.isfile(static_path):
            return static_path
    
    return None
