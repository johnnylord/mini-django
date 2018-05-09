from importlib import import_module
from functools import wraps
from utils.module_loading import import_string
from utils.loggit import register
from utils.color import Color
import settings

class BaseHandler:
    _middleware_chain = None 

    @register(Color.RED)
    def load_middleware(self):
        """
        最終產物是_middleware_chain,是request的進入點
        _middleware_chain是由一層一層的middleware的object所建構出來的object
        """
        #最底層處理request的function,還未經過middleware包裝
        handler = self._get_response 

        #根據settings.MIDDLEWARE的參數將handler做包裝
        for middleware_path in settings.MIDDLEWARE:
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

        response = [
            '%s: %s' % (key, value) for key, value in sorted(request.items())
        ]
        response = '\n'.join(response)
        return response #return回上一層的middleware並且執行process_response,再一層一層的
