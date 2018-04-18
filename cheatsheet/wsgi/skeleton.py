from wsgiref.simple_server import make_server

# The application interface is a callable object
def application(environ, start_response):
    """
    [input]
    - environ
      a dict which is populated by the server for each request

    - start_response
      a callable object developer use to return the status code and response header
    
    [output]
    - strings that are wrapped in an iterable
    """
    
    # Build the response body possibly
    response_body = [
            '%s: %s' % (key, value) for key, value in sorted(environ.items())
        ]
    
    print(response_body)
    response_body = '\n'.join(response_body)
    print(response_body)

    # HTTP response code and message
    status = '200 OK'

    # HTTP headers expected by the client
    # They must be wrapped as a list of tupled pairs
    response_headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(response_body)))
        ]

    # Send status code and response header to the server
    start_response(status, response_headers)

    # Return the response body.
    return response_body 

# Instantiate the server
httpd = make_server('localhost', 8000, application)

httpd.handle_request()
