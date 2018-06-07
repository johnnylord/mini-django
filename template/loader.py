import os

from importlib import import_module

try:
    setting_path = os.environ.get('SETTING_MODULE')
    settings = import_module(setting_path)
except:
    pass

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
