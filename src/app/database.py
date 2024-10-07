from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

def make_database_connection(connection_string):
    client = MongoClient(connection_string)

    return client.mentorHub

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
                    "id": {
                        "$toString": '$_id'
                    }
                }
            },
            {
                "$set": {
                    "resources": {
                        "$map": {
                            "input": '$resources',
                            "as": 'resource',
                            "in": {
                                "id": {
                                    "$toString": '$$resource._id'
                                },
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
                    '_id': 0,
                    'lastSaved': 0,
                    'resources_skills': 0,
                    'skills.lastSaved': 0,
                    'skills._id': 0
                }
            }
    ]

    return dumps(list(db.topics.aggregate(pipeline))[0])

def find_topics(db):
    return dumps(list(db.topics.find({}, { 'id': { "$toString": '$_id' }, 'name': 1, '_id': 0 })))
