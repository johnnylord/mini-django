from middleware.mixin import MiddlewareMixin

class TestModule(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        
    def process_request(self,request):
        pass
        
    def process_response(self,request,response):
        return response