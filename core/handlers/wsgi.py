from cgi import parse_qs
from http.client import responses

from utils.color import Color
from utils.loggit import register
from core.handlers import base

class WSGIRequest:
    """A wrapper class for the incoming request

    [Description]:
        A wrapper object of the reqeust containing essential information
    of incoming request.
    """
    def __init__(self, environ):
        """Construct a wsgi request object

        [Keyword arguments]:
        environ --- a dictionary keeping all the information of the header of
                    the request

        [Attribute]:
        enviorn --- the environ object that passed from WSGI server
        path_info --- url information
        query_string --- a dictionary keeping the query information
        method --- request method
        content_type --- the type of request body
        content_length --- the size of the request body
        server_name --- the requested server's name
        server_port --- the port of the requested server
        server_protocol --- the protocol of communication(ex: HTTP1.1)
        
        [Description]:
            Extract essential information from the environ.
        """
        self.environ = environ
        self.method = environ.get('REQUEST_METHOD').lower()
        self.content_type = environ.get('CONTENT_TYPE', '')

        content_length = environ.get('CONTENT_LENGTH')
        if content_length == '':
            self.content_length = 0
        else:
            self.content_length = int(content_length)

        self.server_name = environ.get('SERVER_NAME')
        self.server_port = int(environ.get('SERVER_PORT'))
        self.server_protocol = environ.get('SERVER_PROTOCOL')

        # Reconstruct the path_info so that there is no '/' at the beginning
        # of path_info and there always be a '/' at the end of the path_info
        path_info = self._get_path_info(environ)
        self.path_info = self._reconstruct_path(path_info)
        
        # Extract the query string
        self.query_string = parse_qs(self._get_query_string(environ))
        print(self)

    def _get_bytes_from_wsgi(self, environ, key, default):
        """Extract the value from the environ with original bytes string
        
        [Key arguments]:
        environ --- the dictionary keeping the information of the request
                    passed from the WSGI server
        key --- the item you wanna extract from the environ
        default --- the default value for the item you wanna extract
        """
        value = environ.get(key, default)
        
        # Non-ASCII values in the WSGI environ, like '中文' are arbitrarily 
        # decoded with ISO-8859-1 method. This is wrong for python website
        # where UTF-8 is the default encoding method. Re-encode to recover 
        # the original bytestring.
        return value.encode('iso-8859-1')

    def _get_path_info(self, environ):
        """Return url PATH_INFO as a string with correct encoding"""
        path = self._get_bytes_from_wsgi(environ, 'PATH_INFO', '/')
        
        return path.decode()
    
    def _get_query_string(self, environ):
        """Return get/post query string with correct encoding"""
        if self.method == 'get':
            query_string = self._get_bytes_from_wsgi(environ, 'QUERY_STRING', '')
            return query_string.decode()
        elif self.method == 'post':
            query_string = environ['wsgi.input'].read(self.content_length)  
            return query_string

    def _reconstruct_path(self, path_info):
        """Reconstruct the url path info

        [Description]:
            Convert the url path_info to the format we want.
        """
        # Check the end of the path_info
        if path_info.endswith('/'):
            pass
        else:
            path_info += '/'

        # Remove the starting '/'
        path_info = path_info[1:]
        return path_info

    def __str__(self):
        query_string = ', '.join(
                [k+"="+str(v) for k, v in self.query_string.items()]
                )
        message = (
            Color.WARNING
            + '[Request Info]: '
            + self.path_info
            + " | "
            + self.method
            + ": "
            + query_string
            + '\n'
            + Color.ENDC
            )
        return message

class WSGIResponse:
    """A wrapper class for response to WSGIServer

    [Description]:
    A wrapper object that contain information of WSGIServer need,
    ex.status, content, content-type and header
    """
    status_code = 200

    def __init__(self, content = b'', content_type=None, status=None):
        """Construct a wsgi response object

        [Keyword argument]:
        content --- content of response body
        content_type --- type of the cotent of response body
        status --- the status of response body

        [Attribute]:
        _headers --- a dictionary to save all response header
        status_code --- response status
        _reason_phrase --- response status phrase
        content --- content of response body

        [Description]:
        extract information from keyword argument, if keyword argument is none,then give default value 
        """
        self._headers = {}
        if status is not None:
            try:
                self.status_code = int(status)
            except (ValueError, TypeError):
                raise TypeError('HTTP status code must be an integer.')

            if not 100 <= self.status_code <= 599:
                raise ValueError('HTTP status code must be an integer from 100 to 599.')
        self._reason_phrase = None

        if content_type is None:
            content_type = "text/plain"

        self['Content-Type'] = content_type
        self.content = content

    @property
    def content(self):
        """Let content method be a property, and return content of _container"""
        return b''.join(self._container)

    @content.setter
    def content(self, value):
        """Save value into _container
        
        [Keyword argument]:
        value --- content that user want to save into content of response body 

        """
        content = self.make_bytes(value)
        self._container = [content]

    @property
    def reason_phrase(self):
        """Return status constant

        [Description]:
        return _reason_phrase which is save status constant, 
        if _reason_phrase ,via status code value to get status constant and return 
        """
        if self._reason_phrase is not None:
            return self._reason_phrase
        return responses.get(self.status_code,'Unknown Status Code')


    @reason_phrase.setter
    def reason_phrase(self, value):
        """Save status constant into _reason_phrase

        [Keyword argument]:
        value --- save status constant into _reason_phrase 
        """
        self._reason_phrase = value


    def make_bytes(self, value):
        """Casting value into bytes type ,then it can correspond with WSGIServer

        [Keyword argument]:
        value --- the value you want to cast to bytes type

        [Description]:
        Because WSGIServer only receive content which is bytes type, you need to cast the value to bytes type
        """
        if isinstance(value,bytes):
            return bytes(value)
        if isinstance(value,str):
            return bytes(value.encode('utf-8'))
        
        return bytes(value)

    def __iter__(self):
        """Return a iteritor of _container to WSGIServer"""
        return iter(self._container)

    def __len__(self):
        """Return the length of content"""
        return len(self.content)

    def __setitem__(self, header, value):
        """Save key value in _headers
        
        [Keyword argument]:
        header --- the key you want to save in dictionary
        value --- the value you want to save in dictionary
        """
        self._headers[header.lower()] = (header,value)

    def __getitem__(self, header):
        """Return key value in _headers
        
        [Keyword argument]:
        header --- the key you want search in _header dictionary
        """
        return self._headers[header.lower()][1]
    
    def items(self):
        """Return a list of dict of _headers"""
        return self._headers.values()


class WSGIHandler(base.BaseHandler):
    """Interface between the WSGI application and the WSGI server
    
    [Description]: 
    The callable object which is the interface between
    the WSGI application and the WSGI server.
    """
    def __init__(self, *args, **kwargs):
        """Construct a WSGIHandler object

        [Description]:
        Construct a WSGIHandler object ,and load middleware from settings.MIDDLEWARE
        """
        super().init(*args, **kwargs);
        self.load_middleware()

    @register()
    def __call__(self, environ, start_response):
        """Receive the request from WSGIServer, and return WSGIResponse to WSGIServer

        [Keyword argument]:
        environ --- a dictionary keeping all the information of the header of
                    the request
        start_response --- the function that return response status and response header to WSGIServer

        [Description]:
        Process the request from WSGIServer. The entry point to middleware, template engine and url router so on
        and return response to WSGIServer

        [Return]:
        WSGIResponse object
        """
        request = WSGIRequest(environ)

        # Process the request and get a response
        response = self.get_response(request)
    
        # Response message
        status = '%d %s' % (response.status_code, response.reason_phrase)
        response['Content-Length'] = str(len(response))
        response_headers = list(response.items())
        
        # Return the metadata of the response via the function
        # provided from WSGI server
        start_response(status, response_headers)
        
        # Return response body
        return response
