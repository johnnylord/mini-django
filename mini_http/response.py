from http.client import responses


class HttpResponseBase:
    status_code = 200

    def __init__(self,content_type=None, status=None):
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
    def reason_phrase(self,value):
        self._reason_phrase = value



    def make_bytes(self,value):
        """
        change value into bytes type ,then it can correspond wsgi response
        """
        if isinstance(value,bytes):
            return bytes(value)
        if isinstance(value,str):
            return bytes(value.encode('utf-8'))
        
        return force_bytes(value)

    def __setitem__(self,header,value):
        self._headers[header.lower()] = (header,value)

    def __getitem__(self,header):
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



class HttpResponse(HttpResponseBase):
    def __init__(self,content = b'',*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.content = content


    @property
    def content(self):
        """
        response content
        """
        return b''.join(self._container)


    @content.setter
    def content(self,value):
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