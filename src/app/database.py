from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import loads
import json
import datetime

def make_database_connection(connection_string):
    client = MongoClient(connection_string)

    return client.mentorHub

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (ObjectId, datetime.datetime)):
            return str(obj)

def find_topic_by_id(db, topic_id):
    pipeline = [
            { "$match": { '_id': ObjectId(topic_id) } },
            {
                "$lookup": {
                    "from": 'resources',
                    "localField": 'resources',
                    "foreignField": '_id',
                    "as": 'resources'
                }
            },
            {
                "$lookup": {
                    "from": 'skills',
                    "localField": 'skills',
                    "foreignField": '_id',
                    "as": 'skills'
                }
            },
            {
                "$lookup": {
                    "from": 'skills',
                    "localField": 'resources.skills',
                    "foreignField": '_id',
                    "as": 'resources_skills'
                }
            },
            {
                "$set": {
                    "resources": {
                        "$map": {
                            "input": '$resources',
                            "as": 'resource',
                            "in": {
                                "_id": '$$resource._id',
                                "name": '$$resource.name',
                                "status": '$$resource.status',
                                "description": '$$resource.description',
                                "duration": '$$resource.duration',
                                "link": '$$resource.link',
                                "skills": {
                                    "$filter": {
                                        "input": '$resource_skills',
                                        "as": 'skill',
                                        "cond": {
                                            "$in": [ '$$skill._id', '$$resource.skills' ]
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            {
                "$addFields": {
                    'resources.skills': '$resource_skills'
                    }
                },
            {
                "$project": {
                    'lastSaved': 0,
                    'resources_skills': 0,
                    'skills.lastSaved': 0,
                    'skills._id': 0
                }
            }
    ]

    return json.dumps(list(db.topics.aggregate(pipeline))[0], cls=MongoJSONEncoder)

def find_topics(db):
    return json.dumps(list(db.topics.find({}, { '_id': 1, 'name': 1 })), cls=MongoJSONEncoder)

def find_paths(db):
    return json.dumps(list(db.paths.find({}, { '_id': 1, 'name': 1 })), cls=MongoJSONEncoder)

def find_path_by_id(db, path_id):
    pipeline = [
        { "$match": { '_id': ObjectId(path_id) } },
        {
            "$lookup": {
                "from": 'topics',
                "localField": 'segments.topics',
                "foreignField": '_id',
                "as": 'topics'
            }
        },
        {
            "$set": {
                "segments": {
                    "$map": {
                        "input": '$segments',
                        "as": 'segment',
                        "in": {
                            "name": '$$segment.name',
                            "topics": {
                                "$filter": {
                                    "input": '$topics',
                                    "as": 'topic',
                                    "cond": {
                                        "$in": [ '$$topic._id', '$$segment.topics' ]
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        {
            "$addFields": {
                'segments.topics': '$topics.name'
            }
        },
        {
            "$project": {
                'topics': 0
            }
        }
    ]

    return json.dumps(list(db.paths.aggregate(pipeline))[0], cls=MongoJSONEncoder)

def insert_topic(db, topic):
    result = db.topics.insert_one(loads(topic))

    return json.dumps(list(db.topics.find_one({ '_id': result.inserted_id }))[0], cls=MongoJSONEncoder)
