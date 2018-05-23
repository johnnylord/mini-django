from utils.loggit import register
from core.handlers import base
from mini_http.response import HttpResponse

class WSGIRequest:
    """
    A wrapper object of the reqeust.
    Contain essential information of the request.
    """
    # WSGI standard variable
    reqeust_method = None
    path_info = None
    query_string = None
    content_type = None
    content_length = None
    server_name = None
    server_port = None
    server_protocol = None
    # No use: script_name = None
    
    def __init__(self, environ):
        self.environ = environ
        self.path_info = get_path_info(environ)
        self.method = environ.get('REQUEST_METHOD')
        self.content_type = environ.get('CONTENT_TYPE', '')
        self.content_length = environ.get('CONTENT_LENGTH', '')
        self.server_name = environ.get('SERVER_NAME')
        self.server_port = environ.get('SERVER_PORT')
        self.server_protocol = environ.get('SERVER_PROTOCOL')

class WSGIHandler(base.BaseHandler):
    """
    THe callable object that is the interface between
    the WSGI application and the WSGI server.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_middleware()

    @register()
    def __call__(self, environ, start_response):

        request = WSGIRequest(environ)
        response = self.get_response(request)
    
        status = '%d %s' % (response.status_code, response.reason_phrase)
        response['Content-Length'] = str(len(response))
        response["Content-Type"] = "text/html"
        response_headers = list(response.items())
    
        start_response(status, response_headers)
        
        return response

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#           Helper function
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def get_bytes_from_wsgi(environ, key, default):
    """
    Get a value from the WSGI environ dictionary as bytes.
    Key and default should be string
    """
    value = environ.get(key, default)
    
    # Non-ASCII values in the WSGI environ, like '中文' are arbitrarily decoded
    # With ISO-8859-1 method. This is wrong for python website where UTF-8 is
    # the default encoding method.
    # Re-encode to recover the original bytestring
    # print(value.encode('iso-8859-1'))
    return value.encode('iso-8859-1')


def get_path_info(environ):
    """
    Return HTTP request's PATH_INFO as a string
    """
    path = get_bytes_from_wsgi(environ, 'PATH_INFO', '/')
    
    return path.decode()
