import os 
from .codegen import CodeBuilder

class SettingTemplate:
    """Project setting template

    [Public attributes]:
    FILES --- The information of the project setting directory

    [Description]:
    Help construct a project setting directory 
    """
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
        """Construct a project setting template

        [Keyword arguments]:
        path --- construct project setting directory under this path
        project_name --- the name the of project setting directory

        [Attribute]:
        path --- construct project setting directory under this path
        project_name --- the name the of project setting directory
        project_dir --- the combination of path and project_name
        """
        self.path = path
        self.project_name = project_name
        self.project_dir = path +"/"+ project_name

    def _render_list(self, coder, args):
        """helper function to render list item in the source code

        [Keyword arguments]:
        coder --- the Codebuilder object
        args --- the list to render
        """
        # Indent the coder
        coder.indent()
        
        # Iterate throught the list item
        for arg in args:
            # Call _render_list recursively if there is another
            # list item in the args list
            if type(arg) is list:
                self._render_list(coder, arg)
            else:
                coder.add_line(arg)
        
        # Dedent the coder
        coder.dedent()
            
    def render(self, f, source_code):
        """Render the python source code in a file

        [Keyword arguments]:
        f --- file object which the source code written in it
        source_code --- python source code
        """
        coder = CodeBuilder()
        for line in source_code:
            if type(line) == list:
                self._render_list(coder, line)
                continue
            elif line.startswith("URL_ROOT") and self.project_name != "project":
                line = 'URL_ROOT = \"{}.urls\"'.format(self.project_name)
            else:
                pass
            coder.add_line(line)
        f.write(str(coder)) 

    def construct(self):
        """Render all the file in the project setting directory"""
        try:
            os.mkdir(self.project_dir)
            for fpath, source_code in self.FILES.items():
                with open(self.project_dir+"/"+fpath, 'w') as f:
                    self.render(f, source_code)
        except:
            raise


class AppTemplate:
    """Project app template

    [Public attributes]:
    FILES --- The information of the app directory

    [Description]:
    Help construct a app directory 
    """
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
        """Construct a app template

        [Keyword arguments]:
        path --- construct app directory under this path
        app_name --- the name the of app directory

        [Attribute]:
        path --- construct app directory under this path
        app_name --- the name the of app directory
        app_dir --- the combination of path and app_name
        """
        self.path = path
        self.app_name = app_name
        self.app_dir = path +"/"+ app_name

    def _render_list(self, coder, args):
        """helper function to render list item in the source code

        [Keyword arguments]:
        coder --- the Codebuilder object
        args --- the list to render
        """
        coder.indent()
        for arg in args:
            if type(arg) == list:
                self._render_list(coder, arg)
                continue
            coder.add_line(arg)
        coder.dedent()
            
    def render(self, f, source_code):
        """Render the python source code in a file

        [Keyword arguments]:
        f --- file object which the source code written in it
        source_code --- python source code
        """
        coder = CodeBuilder()

        for line in source_code:
            if type(line) == list:
                self._render_list(coder, line)
                continue
            coder.add_line(line)
        f.write(str(coder)) 

    def construct(self):
        """Render all the file in the project setting directory"""
        try:
            os.mkdir(self.app_dir)
            for fpath, source_code in self.FILES.items():
                with open(self.app_dir + "/" + fpath, 'w') as f:
                    self.render(f, source_code)
        except:
            raise

