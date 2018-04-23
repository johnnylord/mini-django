from importlib import import_module
from functools import wraps

class BaseHandler:
    _middleware_chain = None
    def load_middleware(self):
        print("load middleware")
        class_name = "TestModule"
        module = import_module("test_module.test_module")
        
        middleware = getattr(module,class_name)

        handler = convert_exception_to_response(self._get_response)
        mw_instance = middleware(handler)
        print(middleware)   
        # handler = convert_exception_to_response(middleware) 

        self._middleware_chain = convert_exception_to_response(mw_instance)


    def get_response(self,request):
        print("middleware get response")
        response = self._middleware_chain(request)
        return response

    def _get_response(self, request):
        """
        Resolve and call the view, then apply view, exception, and
        template_response middleware. This method is everything that happens
        inside the request/response middleware.
        """
        response = None
        return response



def convert_exception_to_response(get_response):
    @wraps(get_response)
    def inner(request):
        response = get_response(request)
        return response
    return inner

        