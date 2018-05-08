from utils.mixin import MiddlewareMixin
import settings
import re


host_validation_re = re.compile(r"^([a-z0-9.-]+|\[[a-f0-9]*:[a-f0-9\.:]+\])(:\d+)?$")


class SecurityMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.redirect = settings.SECURE_SSL_REDIRECT

    def process_request(self, request):
        #httprequest object?
        if self.redirect and request['HTTP_HOST'] and request['wsgi.url_scheme'] != "https":
            host = get_host(request)
            # return HttpResponsePermanentRedirect to https


    def process_response(self, request, response):
        return response


    def get_host(self,request):
        if 'HTTP_HOST' in request:
            host = request['HTTP_HOST']
        
        allowed_hosts = settings.ALLOWED_HOSTS
        if not allowed_hosts:
            allowed_hosts = ['localhost', '127.0.0.1', '[::1]']

        domain,port = split_domain_port(host)
        if domain and validate_host(domain, allowed_hosts):
            return host



    def split_domain_port(host):
        host = host.lower()

        if not host_validation_re.match(host):#要符合regex
            return '', ''

        if host[-1] == ']':
            # It's an IPv6 address without a port.
            return host, ''

        bits = host.rsplit(':', 1)
        domain, port = bits if len(bits) == 2 else (bits[0], '')#檢查有沒有port
        domain = domain[:-1] if domain.endswith('.') else domain
        return domain, port

    def validate_host(host, allowed_hosts):
        for pattern in allowed_hosts:
            if pattern == '*' or pattern == host:
                return True
        
        return False