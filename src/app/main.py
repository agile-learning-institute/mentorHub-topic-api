from flask import Flask, request
from database import *
import os
import pymongo.errors

app = Flask(__name__)

db = make_database_connection(os.getenv('CONNECTION_STRING', 'mongodb://root:example@mentorhub-mongodb:27017/?tls=false&directConnection=true'))

def hello_world(**kwargs):
    return "Hello, World!"

@app.errorhandler(pymongo.errors.WriteError)
def write_error_handler(error):
    app.logger.error(error)
    return "Write Error Occured", 500

@app.get("/api/topic")
def get_topics():
    response = app.make_response(find_topics(db))

    response.content_type = 'application/json'

    return response

@app.post("/api/topic")
def post_topic():
    response = app.make_response(insert_topic(db, request.data))

    response.content_type = 'application/json'

    return response

@app.get("/api/topic/<topicid>")
def get_topic_by_id(topicid):
    response = app.make_response(find_topic_by_id(db, topicid))

    response.content_type = 'application/json'

    return response

@app.get("/api/path")
def get_paths():
    response = app.make_response(find_paths(db))

    response.content_type = 'application/json'

    return response

@app.get("/api/path/<pathid>")
def get_path_by_id(pathid):
    response = app.make_response(find_path_by_id(db, pathid))

    response.content_type = 'application/json'

    return response

app.add_url_rule("/api/topic/<topicid>", methods=["PATCH"], view_func=hello_world)
app.add_url_rule("/api/topic/<topicid>/resource", methods=["POST"], view_func=hello_world)
app.add_url_rule("/api/topic/<topicid>/resource/<resourceid>", methods=["PATCH","DELETE"], view_func=hello_world)
app.add_url_rule("/api/path", methods=["POST"], view_func=hello_world)
app.add_url_rule("/api/path/<pathid>", methods=["PATCH"], view_func=hello_world)
app.add_url_rule("/api/health", methods=["GET"], view_func=hello_world)
app.add_url_rule("/api/config", methods=["GET"], view_func=hello_world)
