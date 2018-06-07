import os 
from .codegen import CodeBuilder

class SettingTemplate:

    FILES = {
        'settings.py':[
            'import os\n',
            'BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n',
            'URL_ROOT = "project.urls"\n',
            'MIDDLEWARE = [',
            [
                repr('middleware.TestModule.TestModule')+",",
                repr('middleware.security.SecurityMiddleware')+",",
            ],
            ']\n',
            'ALLOWED_HOSTS = [',
            ']\n',
            'INSTALLED_APPS = [',
            [
            ],
            ']\n',
            'TEMPLATES = [',
            [
                '{',
                [
                    repr('DIRS')+" : [],",  
                ],
                '},',
            ],
            ']\n',
            'SECURE_SSL_REDIRECT = False',
            'SECURE_HSTS_SECONDS = False',
            'SECURE_HSTS_INCLUDE_SUBDOMAINS = False',
            'SECURE_HSTS_PRELOAD = False',
            'SECURE_CONTENT_TYPE_NOSNIFF = False\n',
            'STATIC_URL = '+repr('/static/'),
        ],

        'urls.py':[
            'from urls.resolver import url\n',
            'urlpatterns = [',
            [
                'url("/index/", index)'+",",
            ],
            ']',
        ],

        '__init__.py':[],
    }

    def __init__(self, path=".", project_name="project"):
        self.path = path
        self.project_name = project_name
        self.project_dir = path +"/"+ project_name

    def _render_list(self, coder, args):
        coder.indent()
        for arg in args:
            if type(arg) == list:
                self._render_list(coder, arg)
                continue
            coder.add_line(arg)
        coder.dedent()
            
    def render(self, f, source_code):
        coder = CodeBuilder()

        for line in source_code:
            if type(line) == list:
                self._render_list(coder, line)
                continue

            if line.startswith("URL_ROOT") and self.project_name != "project":
                line = "URL_ROOT = {}.urls".format(repr(self.project_name))

            coder.add_line(line)
        f.write(str(coder)) 

    def construct(self):
        # Create the project setting directory
        try:
            os.mkdir(self.project_dir)
            for fpath, source_code in self.FILES.items():
                with open(self.project_dir+"/"+fpath, 'w') as f:
                    self.render(f, source_code)

        except Exception as exception:
            print("Exception type", type(exception).__name__)
            print(str(exception))
            return


class AppTemplate:

    FILES = {
        'urls.py':[
            'from urls.utils import url\n',
            'urlpatterns = [',
            [
                'url("/index/", index)'+",",
            ],
            ']',
        ],
        'views.py':[
            'def index(request):',
            [
                'pass',
            ],
        ],

        '__init__.py':[]
    }
    
    def __init__(self, path=".", app_name="home"):
        self.path = path
        self.app_name = app_name
        self.app_dir = path +"/"+ app_name

    def _render_list(self, coder, args):
        coder.indent()
        for arg in args:
            if type(arg) == list:
                self._render_list(coder, arg)
                continue
            coder.add_line(arg)
        coder.dedent()
            
    def render(self, f, source_code):
        coder = CodeBuilder()

        for line in source_code:
            if type(line) == list:
                self._render_list(coder, line)
                continue
            coder.add_line(line)
        f.write(str(coder)) 

    def construct(self):
        # Create the project setting directory
        try:
            os.mkdir(self.app_dir)
            for fpath, source_code in self.FILES.items():
                with open(self.app_dir + "/" + fpath, 'w') as f:
                    self.render(f, source_code)

        except Exception as exception:
            print("Exception type", type(exception).__name__)
            print(str(exception))
            return

