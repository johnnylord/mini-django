import os
import sys
import json
from utils.color import Color
from utils.template.project import SettingTemplate, AppTemplate
from core.handlers.wsgi import WSGIHandler
from wsgiref.simple_server import make_server


def usage():
    """
    Hint for the usage of manage.py
    """
    # Correct format of python manage [option]
    print(Color.WARNING + "Usage: python manage.py [option]" + Color.ENDC)
    
    # List out the supported cmds
    print(Color.RED, "\noption:", Color.ENDC)
    for cmd, info in SUPPORT_CMD.items():
        print(Color.YELLOW, "\t%s" % cmd, Color.ENDC, end=" ")

        # Argument information
        pairs = zip(info['types'], info['kwargs'].keys())
        for pair in pairs:
            print("[{}::{}] ".format(pair[0].__name__, pair[1]), end="")
        print("")


def runserver(port):
    """
    Run a server on a specific port number
    """
    try:
        print(Color.GREEN + "\nRun server at {}:{}\n".format('localhost', port) + Color.ENDC)
        httpd = make_server('localhost', port, WSGIHandler())
        httpd.serve_forever()
    except Exception as exception:
        print("Exception type", type(exception).__name__)
        print(str(exception))


def start_app(app_name):
    """
    create a app template for the user
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app = AppTemplate(base_dir, app_name)
    app.construct()
    
    

def start_project(project_name):
    """
    create a project template for the user
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project = SettingTemplate(base_dir, project_name)
    project.construct()


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
    if len(sys.argv) == 1 or not sys.argv[1] in SUPPORT_CMD.keys():
        usage()
        sys.exit() 
    
    # Execute the command
    cmd = SUPPORT_CMD.get(sys.argv[1])

    if len(sys.argv) > 2:
        # Cast the input to its correct type
        try:
            sys_args = sys.argv[2:]
            types = cmd['types']
            args = [ pair[0](pair[1]) for pair in zip(types, sys_args) ]
            cmd['function'](*args)
        except Exception as exception:
            usage()
            sys.exit()
    else:
        cmd['function'](**cmd['kwargs'])
