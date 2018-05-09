from utils.loggit import register
from core.handlers import base

class WSGIHandler(base.BaseHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_middleware()

    @register()
    def __call__(self, environ, start_response):
        response = self.get_response(environ)
        status = '200 OK'
        response_headers = [
                ('Content-Type', 'text/plain'),
                ('Content-Length', str(len(response)))
            ]
        start_response(status, response_headers)
        #start_response('302 found', [('Location','https://tw.yahoo.com/')])

        return [response]
