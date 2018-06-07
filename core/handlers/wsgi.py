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
            + " "
            + self.method
            + " "
            + query_string
            + '\n'
            + Color.ENDC
            )
        return message


class WSGIResponseBase:
    status_code = 200

    def __init__(self, content_type=None, status=None):
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
    
    @property
    def reason_phrase(self):
        """
        via status code value to get status constant 
        """
        if self._reason_phrase is not None:
            return self._reason_phrase
        return responses.get(self.status_code,'Unknown Status Code')

    @reason_phrase.setter
    def reason_phrase(self, value):
        self._reason_phrase = value



    def make_bytes(self, value):
        """
        change value into bytes type ,then it can correspond wsgi response
        """
        if isinstance(value,bytes):
            return bytes(value)
        if isinstance(value,str):
            return bytes(value.encode('utf-8'))
        
        return force_bytes(value)

    def __setitem__(self, header, value):
        self._headers[header.lower()] = (header,value)

    def __getitem__(self, header):
        return self._headers[header.lower()][1]
    
    def items(self):
        return self._headers.values()

def force_bytes(s):
    """
    force any type of content change to bytes type
    """
    if isinstance(s, memoryview):
        return bytes(s)
    if not isinstance(s, str):
        return str(s).encode(encoding, errors)
    else:
        return s.encode(encoding, errors)



class WSGIResponse(WSGIResponseBase):
    def __init__(self, content = b'', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = content

    @property
    def content(self):
        """
        response content
        """
        return b''.join(self._container)

    @content.setter
    def content(self, value):
        content = self.make_bytes(value)
        self._container = [content]

    def __iter__(self):
        """
        when return a response to wsgi server,we need to pass a iteritor,
        so it will return a iterator of self._container
        """
        return iter(self._container)

    def __len__(self):
        return len(self.content)


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
        response_headers = list(response.items())
        
        start_response(status, response_headers)
        
        return response
