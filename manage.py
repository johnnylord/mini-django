import os
import sys
import json
from wsgiref.simple_server import make_server

from utils.color import Color
from utils.template.project import SettingTemplate, AppTemplate
from core.handlers.wsgi import WSGIHandler

os.environ.setdefault('SETTING_MODULE', 'mysite.settings')

def usage():
    """Hint for the usage of manage.py"""
    # Display the basic format of usage
    print(Color.WARNING + "Usage: python manage.py [option]" + Color.ENDC)
    
    # Options
    print(Color.RED + "\noption:" + Color.ENDC)

    # Display supported command
    for cmd, info in SUPPORT_CMD.items():
        # Each command
        print(Color.YELLOW + "\t%s" % cmd + Color.ENDC, end=" ")

        # Each command's options (type, keyword)
        pairs = zip(info['types'], info['kwargs'].keys())

        # Print out the command's options
        for pair in pairs:
            print("[{}::{}] ".format(pair[0].__name__, pair[1]), end="")
        print("")

def runserver(port=8000):
    """Run a server on a specific port number
    
    [Keyword arguments]:
    port --- the port number server binds to(default 8000)
    """
    try:
        # Display server message
        print(
            Color.GREEN
            + "\nRun server at {}:{}\n".format('localhost', port)
            + Color.ENDC
            )

        # Instaniate a server object on specific port
        httpd = make_server('localhost', port, WSGIHandler())
        httpd.serve_forever()
    except Exception as e:
        print(Color.ERROR + str(e) + Color.ENDC)
        raise

def start_app(app_name='home'):
    """Create a app template

    [Keyword arguments]:
    app_name --- the name of the app(default 'home')
    """
    # Get current directory path
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Instantiate a app template object
    app = AppTemplate(base_dir, app_name)

    # Constrcut the app directory
    try:
        app.construct()
    except Exception as e:
        print(Color.ERROR + str(e) + Color.ENDC)
        raise
    
def start_project(project_name='project'):
    """Create a project setting template

    [Keyword arguments]:
    project_name --- the name of the project (default 'project')
    """
    # Get current directory path   
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Instantiate a project setting template object
    project = SettingTemplate(base_dir, project_name)

    # Construct the app directory
    try:
        project.construct()
    except Exception as e:
        print(Color.ERROR + str(e) + Color.ENDC)
        raise

# Supported commands' information
# 
# Command options:
#     runserver [port]
#     startproject [project_name]
#     startapp [app_name]
SUPPORT_CMD = {
    'runserver': {
        'types': [int,],
        'kwargs': { 
            'port': 8000,
        },
        'function': runserver,
    },
    'startproject': {
        'types': [str,],
        'kwargs': {
            'project_name': 'project',
        },
        'function': start_project,
    },
    'startapp': {
        'types': [str,],
        'kwargs': { 
            'app_name': 'home',
        },
        'function': start_app,
    },
}


if __name__ == "__main__":

    # Check the input format is correct
    if len(sys.argv) == 1 or sys.argv[1] not in SUPPORT_CMD.keys():
        usage()
        sys.exit() 
    
    # Execute the command
    cmd = SUPPORT_CMD.get(sys.argv[1])

    if len(sys.argv) > 2:
        # Cast the input to its correct type
        try:
            sys_args = sys.argv[2:]
            types = cmd['types']
            args = [pair[0](pair[1]) for pair in zip(types, sys_args) ]
            cmd['function'](*args)
        except Exception as exception:
            usage()
            sys.exit()
    else:
        cmd['function'](**cmd['kwargs'])
