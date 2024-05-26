from flask import Flask
from database import *

app = Flask(__name__)

db = makeDatabaseConnection()

def hello_world(**kwargs):
    return "Hello, World!"

@app.route("/api/topic", methods=["GET"])
def return_topic_identifiers():
    response = app.make_response(getTopicList(db))

    response.content_type = 'application/json'

    return response

@app.route("/api/topic/<topicid>", methods=["GET"])
def return_topic(topicid):
    response = app.make_response(getTopicById(db, topicid))

    response.content_type = 'application/json'

    return response

@app.route("/api/path", methods=["GET"])
def return_path_identifiers():
    response = app.make_response(getPathList(db))

    response.content_type = 'application/json'

    return response

@app.route("/api/path/<pathid>", methods=["GET"])
def return_path(pathid):
    response = app.make_response(getPathById(db, pathid))

    response.content_type = 'application/json'

    return response

app.add_url_rule("/api/topic", methods=["POST"], view_func=hello_world)
app.add_url_rule("/api/topic/<topicid>", methods=["PATCH"], view_func=hello_world)
app.add_url_rule("/api/topic/<topicid>/resource", methods=["POST"], view_func=hello_world)
app.add_url_rule("/api/topic/<topicid>/resource/<resourceid>", methods=["PATCH","DELETE"], view_func=hello_world)
app.add_url_rule("/api/path", methods=["POST"], view_func=hello_world)
app.add_url_rule("/api/path/<pathid>", methods=["PATCH"], view_func=hello_world)
app.add_url_rule("/api/health", methods=["GET"], view_func=hello_world)
app.add_url_rule("/api/config", methods=["GET"], view_func=hello_world)
