from utils.mixin import MiddlewareMixin
from mini_http.response import HttpResponse
from template.shortcuts import render




class ErrorHandle(MiddlewareMixin):
    def __init__(self):
        pass
    def process_exception(self, request, exception):
        pass
            
