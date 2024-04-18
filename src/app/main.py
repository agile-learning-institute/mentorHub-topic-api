from flask import Flask

app = Flask(__name__)

def hello_world(**kwargs):
    return "Hello, World!"

app.add_url_rule("/api/topic", methods=["GET","POST"], view_func=hello_world)
app.add_url_rule("/api/topic/<topicid>", methods=["GET","PATCH"], view_func=hello_world)
app.add_url_rule("/api/topic/<topicid>/resource", methods=["POST"], view_func=hello_world)
app.add_url_rule("/api/topic/<topicid>/resource/<resourceid>", methods=["PATCH","DELETE"], view_func=hello_world)
app.add_url_rule("/api/path", methods=["GET","POST"], view_func=hello_world)
app.add_url_rule("/api/path/<pathid>", methods=["PATCH"], view_func=hello_world)
app.add_url_rule("/api/health", methods=["GET"], view_func=hello_world)
app.add_url_rule("/api/config", methods=["GET"], view_func=hello_world)
