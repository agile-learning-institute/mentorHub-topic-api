from flask import Flask
import json

app = Flask(__name__)

def hello_world(**kwargs):
    return "Hello, World!"

def response(object):
    with open('/opt/main/_internal/data.json', 'r') as inf:

        data = json.load(inf)

        return json.dumps(data[object])


@app.route("/api/topic", methods=["GET"])
def return_topic_identifiers():
    output = response('topic_identifiers')

    return output

@app.route("/api/topic", methods=["POST"])
@app.route("/api/topic/<topicid>", methods=["GET","PATCH"])
@app.route("/api/topic/<topicid>/resource", methods=["POST"])
@app.route("/api/topic/<topicid>/resource/<resourceid>", methods=["PATCH","DELETE"])
def return_topic(**kwargs):
    output = response('topic')

    return output

@app.route("/api/path", methods=["GET"])
def return_path_identifiers():
    output = response('path_identifiers')

    return output

@app.route("/api/path", methods=["POST"])
@app.route("/api/path/<pathid>", methods=["GET","PATCH"])
def return_path(**kwargs):
    output = response('path')

    return output

app.add_url_rule("/api/health", methods=["GET"], view_func=hello_world)
app.add_url_rule("/api/config", methods=["GET"], view_func=hello_world)
