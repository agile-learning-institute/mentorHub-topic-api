from flask import Flask
from wsgiref.simple_server import make_server
import routes
from database import mongo_io
import pymongo.errors
import signal
import sys
import os

app = Flask(__name__)

@app.errorhandler(pymongo.errors.WriteError)
def write_error_handler(error):
    app.logger.error(error)
    return "Write Error Occured", 500

app.register_blueprint(routes.topic_routes)

with make_server('', 8086, app) as httpd:

    def signal_handler(signum, frame):
        signal.signal(signum, signal.SIG_IGN)
        httpd.socket.close()
        mongo_io.close()
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)

    print('Serving HTTP on port 8086')

    httpd.serve_forever()
