from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import loads
import os
import json
import datetime


class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (ObjectId, datetime.datetime)):
            return str(obj)

class Collections:

    TOPICS = 'topics'

    PATHS = 'paths'

class MongoIO:

    def __init__(self):
        self.db = self._make_database_connection()

    def _make_database_connection(self):
        connection_string = os.getenv('CONNECTION_STRING', 'mongodb://root:example@mentorhub-mongodb:27017/?tls=false&directConnection=true')

        client = MongoClient(connection_string)

        return client.mentorHub

    def find_one(self, collection, id):
        if collection == Collections.TOPICS:
            pipeline = [
                    { "$match": { '_id': ObjectId(id) } },
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

            result = self.db[collection].aggregate(pipeline)

        elif collection == Collections.PATHS:
            pipeline = [
                { "$match": { '_id': ObjectId(id) } },
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

            result = self.db[collection].aggregate(pipeline)

        return json.dumps(list(result)[0], cls=MongoJSONEncoder)

    def find_all(self, collection):
        return json.dumps(list(self.db[collection].find({}, { '_id': 1, 'name': 1 })), cls=MongoJSONEncoder)

    def insert_one(self, collection, data):
        result = self.db[collection].insert_one(loads(data))

        return json.dumps(self.db[collection].find_one({ '_id': result.inserted_id }), cls=MongoJSONEncoder)

    def close(self):
        self.db.close()

mongo_io = MongoIO()
