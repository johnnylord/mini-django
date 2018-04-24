from utils.mixin import MiddlewareMixin

class TestModule(MiddlewareMixin):
    def process_request(self,request):
        print("process_request")
    def process_response(self,request,response):
        print("process_response")
        return response