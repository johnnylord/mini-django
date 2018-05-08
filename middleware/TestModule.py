from utils.mixin import MiddlewareMixin

class TestModule(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        
    def process_request(self,request):
        print("process_request")
        
    def process_response(self,request,response):
        print("process_response")
        #response['Location'] = "https://127.0.0.1:8000/"
        return response