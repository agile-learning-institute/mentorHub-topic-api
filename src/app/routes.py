from flask import Blueprint, request, make_response
from database import mongo_io, Collections

topic_routes = Blueprint('topic_routes', __name__)
mock_routes = Blueprint('mock_routes', __name__)

@topic_routes.after_request
def set_content_type(response):
    if response.status_code == 200:
        response.content_type = 'application/json'
    return response

@topic_routes.get("/api/topic")
def get_topics():
    return make_response(mongo_io.find_all(Collections.TOPICS))

@topic_routes.post("/api/topic")
def post_topic():
    return make_response(mongo_io.insert_one(Collections.TOPICS, request.data))

@topic_routes.get("/api/topic/<topicid>")
def get_topic_by_id(topicid):
    return make_response(mongo_io.find_one(Collections.TOPICS, topicid))

@topic_routes.get("/api/path")
def get_paths():
    return make_response(mongo_io.find_all(Collections.PATHS))

@topic_routes.get("/api/path/<pathid>")
def get_path_by_id(pathid):
    return make_response(mongo_io.find_one(Collections.PATHS, pathid))

@mock_routes.route("/api/topic/<topicid>", methods=["PATCH"])
@mock_routes.route("/api/topic/<topicid>/resource", methods=["POST"])
@mock_routes.route("/api/topic/<topicid>/resource/<resourceid>", methods=["PATCH","DELETE"])
@mock_routes.route("/api/path", methods=["POST"])
@mock_routes.route("/api/path/<pathid>", methods=["PATCH"])
@mock_routes.route("/api/health", methods=["GET"])
@mock_routes.route("/api/config", methods=["GET"])
def hello_world(**kwargs):
    return "Hello, World!"

