import os
from importlib import import_module

def import_string(middleware_path):
    try:
        module_path, class_name = middleware_path.rsplit('.', 1)
    except:
        print("there are unuse path in settings.middleware ")

    module = import_module(module_path)
    
    try:
        return getattr(module, class_name)
    except:
        print("there are some problem in middleware module")