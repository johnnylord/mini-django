import re
import os

from importlib import import_module

from core.handlers.wsgi import WSGIResponseRedirect
from middleware.mixin import MiddlewareMixin
from utils.color import Color
from utils.loggit import register


setting_path = os.environ.get('SETTING_MODULE')
settings = import_module(setting_path)
host_validation_re = re.compile(r"^([a-z0-9.-]+|\[[a-f0-9]*:[a-f0-9\.:]+\])(:\d+)?$")


class SecurityMiddleware(MiddlewareMixin):
    """Middleware to handle the security of request and response

    [Public method]:
    process_request --- Check the request that is HTTPS or HTTP
    process_response --- Set the header of response
    get_host --- Get HTTP_HOST from request

    [Description]:
    User can set flag in settings.py to use different kind of security method
    
    SECURE_SSL_REDIRECT --- if set TRUE, process_request will redirect all non-HTTPS 
    request to HTTPS 
    SECURE_HSTS_SECONDS --- if set non zero number, then will add "HTTP Strict Transport Security" header in response
    SECURE_HSTS_INCLUDE_SUBDOMAINS --- if set TRUE, then add "includeSubDomains" into response header,
    only effective when  SECURE_HSTS_SECONDS is non zero number
    SECURE_HSTS_PRELOAD --- if set TRUE, then add "preload" into response header,only effective 
    when  SECURE_HSTS_SECONDS is non zero number
    SECURE_CONTENT_TYPE_NOSNIFF --- if set non zero number,then add "X-Content-Type-Options: nosniff" into response  
    """
    def __init__(self, get_response=None):
        """Construct the Security middleware, and get the value from settings

        [Keyword argument]
        get_response --- later middleware or the view function
        """
        super().__init__(get_response)
        self.sts_seconds = settings.SECURE_HSTS_SECONDS
        self.sts_include_subdomains = settings.SECURE_HSTS_INCLUDE_SUBDOMAINS
        self.sts_preload = settings.SECURE_HSTS_PRELOAD
        self.redirect = settings.SECURE_SSL_REDIRECT
        self.content_type_nosniff = settings.SECURE_CONTENT_TYPE_NOSNIFF


    @register(Color.PURPLE)
    def process_request(self, request):
        """Check the request is HTTPS or HTTP domain,and decide whether redirect to HTTPS domain

        [Keyword argument]:
        request --- the WSGIRequest object that passed from WSGIHandler
        """
        # if self.redirect and request['HTTP_HOST'] and request['wsgi.url_scheme'] != "https":
        if self.redirect and request.environ['HTTP_HOST'] and request.environ['wsgi.url_scheme'] != "https":
            host = self._get_host(request.environ)
            return WSGIResponseRedirect("https://%s" % host)


    @register(Color.YELLOW)
    def process_response(self, request, response):
        """Add security header to response  
        
        [Keyword argument]:
        request --- the WSGIRequest object that passed from WSGIHandler
        reaponse --- the WSGIResponse object that BaseHandler pass

        [Return]:
        WSGIResponse object
        """
        if (self.sts_seconds and 'strict-transport-security' not in response):
            sts_header = "max-age=%s" % self.sts_seconds      
            if self.sts_include_subdomains:
                sts_header = sts_header + "; includeSubDomains"
            if self.sts_preload:
                sts_header = sts_header + "; preload"
            response["strict-transport-security"] = sts_header

        if self.content_type_nosniff and 'x-content-type-options' not in response:
            response["x-content-type-options"] = "nosniff"

        return response
        

    def _get_host(self,request):
        """Get HTTP_HOST from request and check if it is correspond to ALLOWED_HOSTS in settings.py

        [Keyword argument]:
        request --- the WSGIRequest object that passed from WSGIHandler
        
        [Return]:
        if host is correspond ALLOWED_HOSTS,return host
        """
        if 'HTTP_HOST' in request:
            host = request['HTTP_HOST']
        
        #get ALLOWED_HOST list in settings.py, if user undefined then add default host in allowed_host
        allowed_hosts = settings.ALLOWED_HOSTS
        if not allowed_hosts:
            allowed_hosts = ['localhost', '127.0.0.1', '[::1]']

        domain,port = split_domain_port(host)
        if domain and validate_host(domain, allowed_hosts):
            return host



def split_domain_port(host):
    """Split url into port and domain and return

    [Keyword argument]:
    host --- the HTTP_HOST value in request

    [Return]:
    domain and port which are split from host
    """
    host = host.lower()

    if not host_validation_re.match(host):
        return '', ''

    if host[-1] == ']':
        # It's an IPv6 address without a port.
        return host, ''

    bits = host.rsplit(':', 1)
    #check if there is port
    domain, port = bits if len(bits) == 2 else (bits[0], '')
    domain = domain[:-1] if domain.endswith('.') else domain
    return domain, port


def validate_host(host, allowed_hosts):
    """The domain in host need to correspond ALLOWED_HOST,if it is, it will return True, else False

    [Keyword argument]:
    host --- domain split from HTTP_HOST in request
    allowed_hosts --- the list that user set in settings
    """
    for pattern in allowed_hosts:
        if pattern == '*' or pattern == host:
            return True
    return False
