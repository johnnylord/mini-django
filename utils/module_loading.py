import os
from importlib import import_module

def import_string(middleware_path):
    """Import middleware and return module of the middleware class

    [Keyword argument]:
    middleware_path --- the path in MIDDLEWARE of settings

    [Return]:
    Module of the middleware
    """
    try:
        module_path, class_name = middleware_path.rsplit('.', 1)
    except Exception as e:
        error_message = ("Erro:%s , %s" %  (type(exception).__name__,exception))
        print(error_message)

    module = import_module(module_path)
    
    try:
        return getattr(module, class_name)
    except Exception as e:
        error_message = ("Erro:%s , %s" %  (type(exception).__name__,exception))
        print(error_message)
