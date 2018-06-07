from template.html import HtmlTemplite
from mini_http.response import HttpResponse
import os
from importlib import import_module

setting_path = os.environ.get('SETTING_MODULE')
settings = import_module(setting_path)

class StaticHandler:
    def __init__(self,static_name):
        self.base_dir = settings.BASE_DIR
        self.static_url = settings.STATIC_URL
        self.installed_apps = settings.INSTALLED_APPS

        self.static_name = self.get_static(static_name)



    def get_static(self,static_name):
        for app in self.installed_apps:
            static_path = os.path.join(self.base_dir,app,static_name[1:])
            if os.path.isfile(static_path):
                return static_path
        return None

    def parse_static(self):
        if os.path.isfile(self.static_name) is False:
            pass
        else:
            return HtmlTemplite(self.static_name).render()

    def render(self):
        return HttpResponse(self.parse_static(),content_type = 'text/css')
    