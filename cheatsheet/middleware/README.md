class MiddlewareMixin:
    def __init__(self, get_response=None):
        self.get_response = get_response
        print("module init")
        super().__init__()

    def __call__(self, request):
        print("middleware __call__")
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class TestModule(MiddlewareMixin):
    def process_request(self,request):
        print("process_request")
    def process_response(self,request,response):
        print("process_response")
        return response

先在/usr/local/lib/python3.5/dist-packages/test_module/ 創立一個空的__init__.py檔
再將上面這段code放到/usr/local/lib/python3.5/dist-packages/test_module/test_module.py