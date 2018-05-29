import os 

class SettingTemplate:

    FILES = {
        'settings.py':{
            'import':[],
            'MIDDLEWARE':[
                "'middleware.TestModule.TestModule'",
                "'middleware.security.SecurityMiddleware'",
            ],
            'ALLOWED_HOSTS':[],
            'SECURE_SSL_REDIRECT':True,
            'SECURE_HSTS_SECONDS':False,
            'SECURE_HSTS_INCLUDE_SUBDOMAINS':False,
            'SECURE_HSTS_PRELOAD':False,
            'SECURE_CONTENT_TYPE_NOSNIFF':False,
        },

        'urls.py':{
            'import':[
                'from urls.utils import path',
            ],
            'urlpatterns':[
                'path("/index/", index)',
            ],
        }    
    }

    def __init__(self, path=".", project_name="project"):
        self.path = path
        self.project_name = project_name
        self.project_dir = path +"/"+ project_name

    def render(self, f, context):
        keylist = context.keys()
        keylist = sorted(keylist)

        for key in keylist:
            content = context[key]

            if key == 'import':
                f.write('\n'.join(content))
                f.write('\n\n')
                continue
            
            # Type of content( List, Bool )
            if type(content) == list:
                f.write('\n')
                f.write('{} = [\n'.format(key))
                for line in content:
                    f.write('\t{},\n'.format(line))
                f.write(']\n')

            elif type(content) == bool:
                f.write('\n')
                if content == True:
                    f.write('{} = True\n'.format(key))
                else:
                    f.write('{} = False\n'.format(key))

    def construct(self):
        # Create the project setting directory
        try:
            os.mkdir(self.project_dir)
            for fpath, context in self.FILES.items():
                with open(self.project_dir+"/"+fpath, 'w') as f:
                    self.render(f, context)

        except Exception as exception:
            print("Exception type", type(exception).__name__)
            print(str(exception))
            return


class AppTemplate:

    FILES = {
        'urls.py':{
            'import':[
                'from urls.utils import path',
            ],
            'urlpatterns':[
                'path("/index/", index)',
            ],
        },
        'views.py':{
            'import':[],
            'function':{
                'name':'index',
                'comment':'process request...'
            },
        }
    }
    
    def __init__(self, path=".", app_name="home"):
        self.path = path
        self.app_name = app_name
        self.app_dir = path +"/"+ app_name

    def render(self, f, context):
        keylist = context.keys()
        keylist = sorted(keylist)

        for key in keylist:
            content = context[key]

            if key == 'import':
                f.write('\n'.join(content))
                f.write('\n\n')
                continue

            if key == 'function':
                f.write('def {}(request):\n'.format(content['name']))
                f.write('\t"""\n\t{}\n\t"""\n\tpass'.format(content['comment']))
                continue
 
            # Type of content( List, Bool )
            if type(content) == list:
                f.write('\n')
                f.write('{} = [\n'.format(key))
                for line in content:
                    f.write('\t{},\n'.format(line))
                f.write(']\n')

            elif type(content) == bool:
                f.write('\n')
                if content == True:
                    f.write('{} = True\n'.format(key))
                else:
                    f.write('{} = False\n'.format(key))

    def construct(self):
        # Create the project setting directory
        try:
            os.mkdir(self.app_dir)
            for fpath, context in self.FILES.items():
                with open(self.app_dir + "/" + fpath, 'w') as f:
                    self.render(f, context)

        except Exception as exception:
            print("Exception type", type(exception).__name__)
            print(str(exception))
            return

