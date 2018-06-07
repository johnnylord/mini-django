from utils.mixin import MiddlewareMixin
from importlib import import_module
import re
import os


setting_path = os.environ.get('SETTING_MODULE')
settings = import_module(setting_path)
host_validation_re = re.compile(r"^([a-z0-9.-]+|\[[a-f0-9]*:[a-f0-9\.:]+\])(:\d+)?$")


class SecurityMiddleware(MiddlewareMixin):
    """
    check request if http or https, if user set the flag,
    it will redirect the page to the https domain,or it will add header to let browser
    forbid the http communication or forbid browser to decide which type the response content is. 
    """
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.sts_seconds = settings.SECURE_HSTS_SECONDS
        self.sts_include_subdomains = settings.SECURE_HSTS_INCLUDE_SUBDOMAINS
        self.sts_preload = settings.SECURE_HSTS_PRELOAD
        self.redirect = settings.SECURE_SSL_REDIRECT
        self.content_type_nosniff = settings.SECURE_CONTENT_TYPE_NOSNIFF


    def process_request(self, request):
        if self.redirect and request['HTTP_HOST'] and request['wsgi.url_scheme'] != "https":
            host = self.get_host(request)
            # return HttpResponsePermanentRedirect to https

    def process_response(self, request, response):
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
        

    def get_host(self,request):
        """
        get http host and check if it is correspond to ALLOWED_HOSTS in setting.py
        """
        if 'HTTP_HOST' in request:
            host = request['HTTP_HOST']
        
        #取得setting.py中的ALLOWED_HOST list,如果使用者沒有定義,就將localhost的網址放到預設到allowed_host
        allowed_hosts = settings.ALLOWED_HOSTS
        if not allowed_hosts:
            allowed_hosts = ['localhost', '127.0.0.1', '[::1]']

        domain,port = split_domain_port(host)
        if domain and validate_host(domain, allowed_hosts):
            return host



def split_domain_port(host):
    """
    split url into port and domain and return
    """
    host = host.lower()

    #網址要符合regex格式避免有一些奇怪的亂碼
    if not host_validation_re.match(host):
        return '', ''

    if host[-1] == ']':
        # It's an IPv6 address without a port.
        return host, ''

    #將網址切成domain and port,並且分別return
    bits = host.rsplit(':', 1)
    domain, port = bits if len(bits) == 2 else (bits[0], '')#檢查有沒有port
    domain = domain[:-1] if domain.endswith('.') else domain
    return domain, port


def validate_host(host, allowed_hosts):
    """
    domain need to correspond ALLOWED_HOST,if it is ,will return True,else False
    """
    for pattern in allowed_hosts:
        if pattern == '*' or pattern == host:
            return True
    return False