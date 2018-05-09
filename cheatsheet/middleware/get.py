from wsgiref.simple_server import make_server
import base

# To help parse the query string and retrieve those values
from cgi import parse_qs, escape


html = """
<html>
<body>
    <form method="get" action="">
        <p>
            Age: <input type="text" name="age" value="%(age)s">
        </p>
        <p>
            Hobbies:
            <input name="hobbies" type="checkbox" value="software" %(checked-software)s>
            Software
            <input name="hobbies" type="checkbox" value="tunning" %(checked-tunning)s>
            Auto Tunning
        </p>
        <p>
            <input type="submit" value="Submit">
        </p>
    </form>
    <p>
        Age: %(age)s<br>
        Hobbies: %(hobbies)s
    </p>
</body>
</html>
"""

# class WSGIRequest(HttpRequest):
#     def __init__(self,environ):
#         print("WSGIRequest init")
    
#         self.environ = environ
#         self.path_info = '/'

#         self.META = environ
#         self.META['PATH_INFO'] = '/'


class WSGIHandler(base.BaseHandler):
    def __init__(self,*arg,**kwargs):
        self.load_middleware()
    def __call__(self,environ, start_response):
            # Returns a dictionary in which the values are list
        print("response")
        self.get_response(environ)
        
        d = parse_qs(environ['QUERY_STRING'])
        
        age = d.get('age', [''])[0] # Return the first age value
        hobbies = d.get('hobbies', []) # Returns a list of hobbies
        
        # Always escape user input to avoid script injection
        age = escape(age)
        hobbies = [escape(hobby) for hobby in hobbies ]
        

        print("="*50)
        
        # Build the response body possibly
        response_body = html % { 
                'checked-software': ('', 'checked')['software' in hobbies],
                'checked-tunning': ('', 'checked')['tunning' in hobbies],
                'age': age or 'Empty',
                'hobbies': ','.join(hobbies or ['No Hobbies?'])
            } 
        
        # HTTP response code and message
        status = '200 OK'

        # HTTP headers expected by the client
        # They must be wrapped as a list of tupled pairs
        response_headers = [
                ('Content-Type', 'text/html'),
                ('Content-Length', str(len(response_body)))
            ]

        # Send status code and response header to the server
        start_response(status, response_headers)

        # Return the response body.
        return [bytes(response_body,encoding = "utf8")] 

# Instantiate the server
httpd = make_server('localhost', 8000, WSGIHandler())

httpd.serve_forever()
