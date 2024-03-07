from flask import Flask

app = Flask(__name__)

def hello_world(**kwargs):
    return "Hello, World!"

app.add_url_rule("/api/topic", methods=["GET","POST"], view_func=hello_world)
app.add_url_rule("/api/topic/<id>", methods=["GET","PATCH"], view_func=hello_world)
app.add_url_rule("/api/topic/<id>/resource", methods=["POST"], view_func=hello_world)
app.add_url_rule("/api/topic/<id>/resource/<name>", methods=["PATCH","DELETE"], view_func=hello_world)
app.add_url_rule("/api/health", methods=["GET"], view_func=hello_world)
app.add_url_rule("/api/config", methods=["GET"], view_func=hello_world)

if __name__ == '__main__':
    app.run(host='::', port='8086')
