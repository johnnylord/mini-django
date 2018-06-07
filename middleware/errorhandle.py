from middleware.mixin import MiddlewareMixin
from core.handlers.wsgi import WSGIResponse
from template.shortcuts import render

class ErrorHandle(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)

    def process_exception(self, request, exception):
        error_message = ("Erro:%s , %s" %  (type(exception).__name__,exception))
        return WSGIResponse(error_message)

    def process_response(self, request, response):
        if response is None:
            error_message = "response is None"
            return WSGIResponse(error_message)
        return response
            
