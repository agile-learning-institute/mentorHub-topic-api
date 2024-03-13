from wsgiref.simple_server import make_server
from main import app

with make_server('', 8086, app) as httpd:
    print('Serving HTTP on port 8086')

    httpd.serve_forever()
