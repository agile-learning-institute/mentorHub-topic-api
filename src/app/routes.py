from flask import Blueprint, make_response, request

from database import Collections, mongo_io

topic_routes = Blueprint('topic_routes', __name__)

@topic_routes.after_request
def set_content_type(response):
    if response.status_code == 200:
        response.content_type = 'application/json'
    return response

@topic_routes.get("/api/topic")
def get_topics():
    return make_response(mongo_io.find_all(Collections.TOPICS))

@topic_routes.get("/api/topic/<topicid>")
def get_topic_by_id(topicid):
    return make_response(mongo_io.find_one(Collections.TOPICS, topicid))
