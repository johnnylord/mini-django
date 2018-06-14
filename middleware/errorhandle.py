from middleware.mixin import MiddlewareMixin
from core.handlers.wsgi import WSGIResponse
from template.shortcuts import render

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

    def process_exception(self, request, exception):
        """Return exception response, when exception had been rasie

        [Keyword argument]:
        request --- the WSGIRequest object that passed from WSGIHandler
        exception --- the exception BaseHandler raise

        [Return]:
        WSGIResponse object which content is exception type
        """
        error_message = ("Erro:%s , %s" %  (type(exception).__name__,exception))
        return WSGIResponse(error_message)

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
            
