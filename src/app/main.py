from flask import Flask, request, Blueprint
from database import *
import os
import pymongo.errors

app = Flask(__name__)

db = make_database_connection(os.getenv('CONNECTION_STRING', 'mongodb://root:example@mentorhub-mongodb:27017/?tls=false&directConnection=true'))

topic_routes = Blueprint('topic_routes', __name__)

def hello_world(**kwargs):
    return "Hello, World!"

@topic_routes.after_request
def set_content_type(response):
    if response.status_code == 200:
        response.content_type = 'application/json'
    return response

@app.errorhandler(pymongo.errors.WriteError)
def write_error_handler(error):
    app.logger.error(error)
    return "Write Error Occured", 500

@topic_routes.get("/api/topic")
def get_topics():
    return app.make_response(find_topics(db))

@topic_routes.post("/api/topic")
def post_topic():
    return app.make_response(insert_topic(db, request.data))

@topic_routes.get("/api/topic/<topicid>")
def get_topic_by_id(topicid):
    return app.make_response(find_topic_by_id(db, topicid))

@topic_routes.get("/api/path")
def get_paths():
    return app.make_response(find_paths(db))

@topic_routes.get("/api/path/<pathid>")
def get_path_by_id(pathid):
    return app.make_response(find_path_by_id(db, pathid))

app.register_blueprint(topic_routes)

app.add_url_rule("/api/topic/<topicid>", methods=["PATCH"], view_func=hello_world)
app.add_url_rule("/api/topic/<topicid>/resource", methods=["POST"], view_func=hello_world)
app.add_url_rule("/api/topic/<topicid>/resource/<resourceid>", methods=["PATCH","DELETE"], view_func=hello_world)
app.add_url_rule("/api/path", methods=["POST"], view_func=hello_world)
app.add_url_rule("/api/path/<pathid>", methods=["PATCH"], view_func=hello_world)
app.add_url_rule("/api/health", methods=["GET"], view_func=hello_world)
app.add_url_rule("/api/config", methods=["GET"], view_func=hello_world)
