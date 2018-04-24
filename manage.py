import os
import sys
from core.handlers.wsgi import WSGIHandler
from wsgiref.simple_server import make_server

if __name__ == "__main__":
    try:
        httpd = make_server('localhost', 8000, WSGIHandler())
        httpd.serve_forever()
    except:
        print("there are some trouble with you project")