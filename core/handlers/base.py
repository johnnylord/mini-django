import os
import types
from importlib import import_module
from functools import wraps

from utils.module_loading import import_string
from utils.loggit import register
from utils.color import Color
from urls.resolver import UrlResolver 
from core.exceptions import Http404

try:
    setting_path = os.environ.get('SETTING_MODULE')
    settings = import_module(setting_path)
except:
    pass


class BaseHandler:
    """Provide genernal function to WSGIhandler

    [Public method]
    load_middleware --- load all middleware in a chain
    get_response --- a interface to WSGIHandler
    process_exception_by_middleware --- call process_excception in middleware and get response 

    [Private method]
    _get_response --- process request and return a response 
    
    """
    _middleware_chain = None
    _exception_middleware = None
    @register(Color.RED)
    def load_middleware(self):
        """Load middleware object and save entry point in _middleware_chain

        [Attributes]:
        _exception_middleware --- the list that save all process_exception function in middleware
        _middleware_chain --- the entry point to middleware chain which is a class object

        [Description]:
        Get the list of middleware in settings.py,and make a middleware object to next middleware argument.
        Save outermost layer of middleware in _middleware_chain.
        When user call _middleware_chain ,the requset will pass through to all of middleware and reach _get_response method 
        """
        self._exception_middleware = []

        #the base layer of middleware to process request
        handler = self.convert_exception_to_response(self._get_response) 

        for middleware_path in settings.MIDDLEWARE:
            # import_string() return a middleware class
            middleware = import_string(middleware_path)  
            mw_instance = middleware(handler)
            
            if hasattr(mw_instance,'process_exception'):
                self._exception_middleware.append(mw_instance.process_exception)
            
            handler = self.convert_exception_to_response(mw_instance)

        self._middleware_chain = handler 
        

    def get_response(self,request):
        """A interface for WSGIHandler.

        [Keyword argument]:
        request --- the WSGIRequest object that passed from WSGIHandler

        [Description]:
        WSGIHandler call this method to let request go though middleware and _get_response method to process request
        """
        response = self._middleware_chain(request) #middleware的進入點
        return response

    def _get_response(self, request):
        """Process request to url router ,template engine and return response

        [Keyword argument]:
        request --- the WSGIRequest object that passed from WSGIHandler

        [Return]:
        WSGIResponse object

        [Description]:
        Call url router to get the view function user defined, and get the response that 
        views function returned. If view function return None or error exception, then call 
        process_exception_by_middleware method to handle the exception to return error message response.

        """
        urlRoute = request.path_info
        resolver = UrlResolver(settings.URL_ROOT)
        (args, kwargs, view) = resolver.resolve_url(urlRoute)
    
        if view is None:
            #not found
            raise Http404(
                "The url %s in request didn't match any urlpattern in project." % urlRoute 
            )

        try:
            response = view(request, *args, **kwargs)
        except Exception as e:
            if isinstance(view, types.FunctionType):
                view_name = view.__name__
            else:
                view_name = view.__class__.__name__
            raise ValueError(
                "In view %s there are some error with --- %s" %(view_name,e)
            )

        if response is None:
            if isinstance(view, types.FunctionType):
                view_name = view.__name__
            else:
                view_name = view.__class__.__name__

            raise ValueError(
                "The view %s didn't return an HttpResponse object. It "
                "returned None instead." % view_name
            )

        return response

    def process_exception_by_middleware(self, exception, request):
        """Call process_exception in middleware and get error message response

        [Keyword argument]:
        exception --- the exception view function raise 
        request --- WSGIRequest object that passed from WSGIHandler

        [Return]:
        a WSGIResponse object that filled of exception message

        """
        for middleware_method in self._exception_middleware:
            response = middleware_method(request, exception)
            if response:
                return response


    def convert_exception_to_response(self, get_response):
        @wraps(get_response)
        def inner(request):
            try:
                response = get_response(request)
            except Exception as exc:
                response = self.process_exception_by_middleware(exc, request)
            return response
        return inner