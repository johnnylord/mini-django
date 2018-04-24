from importlib import import_module
from functools import wraps
from utils.module_loading import import_string
import settings

class BaseHandler:
    _middleware_chain = None
    def load_middleware(self):
        print("load middleware")

        #假如middleware執行的流程為上到下,則需要從下到上開始create object,將object給他上面的object當作init的參數,有點類似遞迴的概念
        handler = self._get_response#middleware全部執行完後所執行的function
        for middleware_path in settings.MIDDLEWARE:
            middleware = import_string(middleware_path)
            mw_instance = middleware(handler)
            handler = mw_instance

        self._middleware_chain = handler
        
    def get_response(self,request):
        print("middleware get response")
        response = self._middleware_chain(request)
        return response

    def _get_response(self, request):
        #url router doing here
        response = [
            '%s: %s' % (key, value) for key, value in sorted(request.items())
        ]
        response = '\n'.join(response)
        return response
