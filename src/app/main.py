from flask import Flask
from database import *
import os

app = Flask(__name__)

db = make_database_connection(os.getenv('CONNECTION_STRING', 'mongodb://root:example@mentorhub-mongodb:27017/?tls=false&directConnection=true'))

def hello_world(**kwargs):
    return "Hello, World!"

@app.route("/api/topic", methods=["GET"])
def get_topics():
    response = app.make_response(find_topics(db))

    response.content_type = 'application/json'

    return response

@app.route("/api/topic/<topicid>", methods=["GET"])
def get_topic_by_id(topicid):
    response = app.make_response(find_topic_by_id(db, topicid))

    response.content_type = 'application/json'

    return response

app.add_url_rule("/api/topic", methods=["POST"], view_func=hello_world)
app.add_url_rule("/api/topic/<topicid>", methods=["PATCH"], view_func=hello_world)
app.add_url_rule("/api/topic/<topicid>/resource", methods=["POST"], view_func=hello_world)
app.add_url_rule("/api/topic/<topicid>/resource/<resourceid>", methods=["PATCH","DELETE"], view_func=hello_world)
app.add_url_rule("/api/health", methods=["GET"], view_func=hello_world)
app.add_url_rule("/api/config", methods=["GET"], view_func=hello_world)
