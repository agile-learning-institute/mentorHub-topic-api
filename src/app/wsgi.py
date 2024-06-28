from wsgiref.simple_server import make_server
from main import app, db
import signal
import sys

with make_server('', 8086, app) as httpd:

    def signal_handler(signum, frame):
        signal.signal(signum, signal.SIG_IGN)
        httpd.socket.close()
        db.close()
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)

    print('Serving HTTP on port 8086')

    httpd.serve_forever()
