import sys
import os
from importlib import import_module
from pathlib import Path

from middleware.mixin import MiddlewareMixin
from core.handlers.wsgi import WSGIResponse
from template.shortcuts import render
from template.html import HtmlTemplite
from core.exceptions import Http404
from utils.color import Color
from utils.loggit import register

setting_path = os.environ.get('SETTING_MODULE')
settings = import_module(setting_path)

CURRENT_DIR = Path(__file__).parent

class ErrorHandle(MiddlewareMixin):
    """Middleware to handle the exception that BaseHandler class raise
    
    [Description]:
    When url router or WSGIResponse or views function user defined raise exception,
    then return a error page which contain exception information to WSGIHandler 
    """
    def __init__(self, get_response=None):
        """Construct  a ErrorHandle middleware
        
        [Keyword argument]
        get_response --- later middleware and the view
        """
        super().__init__(get_response)

    @register(Color.RED)
    def process_exception(self, request, exception):
        """Return exception response, when exception had been rasie

        [Keyword argument]:
        request --- the WSGIRequest object that passed from WSGIHandler
        exception --- the exception that BaseHandler raises

        [Return]:
        WSGIResponse object which content is exception message
        """

        if isinstance(exception, Http404):
            response = technical_404_response(request, exception)
        else:
            response = technical_500_response(request, *sys.exc_info())

        return response

    @register(Color.YELLOW)
    def process_response(self, request, response):
        """Process response check whether there is error occur
        
        [Keyword argument]:
        request --- the WSGIRequest object that passed from WSGIHandler
        response --- the WSGIResponse object that BaseHandler pass 

        [Return]:
        WSGIResponse object which content is BaseHandler return or error information
        """
        if response is None:
            error_message = "response is None"
            return WSGIResponse(error_message)
        return response

def technical_404_response(request, exception):
    """Return a WSGIResponse with status 404 and exception message

    [Keyword argument]:
    request --- the WSGIRequest object that passed from WSGIHandler
    exception --- the exception raise from view function or url router

    [Return]:
    WSGIResponse object which had loaded 404_exception html file with error message

    """
    error_url = request.path_info
    context = {'request_path':error_url,'reasons':str(exception)}
    
    with Path(CURRENT_DIR, 'templates', 'technical_404.html').open() as fh:
        content = HtmlTemplite(fh.name).render(context)

    return WSGIResponse(content, 'text/html', 404)


def technical_500_response(request, exc_type, exc_value, status_code=500):
    """Return a WSGIResponse with status 500 and exception message

    [Keyword argument]:
    request --- the WSGIRequest object that passed from WSGIHandler
    exc_type --- the type of excetion
    exc_value --- detailed of exception message

    [Return]: 
    WSGIResponse object which had loaded 500_exception html file with error message
    
    """
    context = {'exc_type':str(exc_type)[1:-1],'exc_value':exc_value}
    
    with Path(CURRENT_DIR, 'templates', 'technical_500.html').open() as fh:
        content = HtmlTemplite(fh.name).render(context)

    return WSGIResponse(content, 'text/html', 500)

