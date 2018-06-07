import os
from importlib import import_module
from functools import wraps
from utils.module_loading import import_string
from utils.loggit import register
from utils.color import Color
from mini_http.response import HttpResponse
from urls.resolver import UrlResolver 
from template.static import StaticHandler

class BaseHandler:
    _middleware_chain = None 

    def __init__(self):
        self.setting_path = os.environ.get('SETTING_MODULE')
        self.settings = import_module(self.setting_path)

    @register(Color.RED)
    def load_middleware(self):
        """
        最終產物是_middleware_chain,是request的進入點
        _middleware_chain是由一層一層的middleware的object所建構出來的object
        """
        #最底層處理request的function,還未經過middleware包裝
        handler = self._get_response 

        #根據settings.MIDDLEWARE的參數將handler做包裝
        for middleware_path in self.settings.MIDDLEWARE:
            middleware = import_string(middleware_path) # import_string() return a middleware class 
            mw_instance = middleware(handler) # init handler 
            handler = mw_instance


        #當middleware一層一層的包起來之後會將最外層的middleware存在_middleware_chain,
        #在get_response()中呼叫,request開始進入middleware
        self._middleware_chain = handler 
        
    def get_response(self,request):
        """
        a interface for WSGIHandler,
        真正處理request的是middleware中的process_request(),process_response() ,and _get_response()
        """
        response = self._middleware_chain(request) #middleware的進入點
        return response

    def _get_response(self, request):
        """
        1. url router doing here and return view function and the information in the url
        2. process_view in middleware are called to enforce view function
        3. call view function and get view function response
        4. if response if None print error ,may return an error page to browser
        5. if response has render ,and call process_template_response
        6. return response to browser
        """
        # get request url
        urlRoute = request.path_info
        if urlRoute.startswith("/static"):
            static = StaticHandler(urlRoute)
            return static.render()
        resolver = UrlResolver(self.settings.URL_ROOT)
        (args, kwargs, view) = resolver.resolve_url(urlRoute)
        # response = view(request, *args, **kwargs)
        if view == None :
            response = """
            <html>
                <head>
                    <title>Test</title>
                </head>
                <body>
                Hello World
                </body>
            </html>
            """
            response = '\n'.join(response)
            response = HttpResponse(response) 
            response["Content-Type"] = "text/html"
        else :
            response = view(request)
        #return回上一層的middleware並且執行process_response,再一層一層的
        return response
