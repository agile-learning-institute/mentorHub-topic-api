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
                "$set": {
                    "id": {
                        "$toString": '$_id'
                    }
                }
            },
            {
                "$project": {
                    '_id': 0,
                }
            }
    ]

    return dumps(list(db.topics.aggregate(pipeline))[0])

def find_topics(db):
    return dumps(list(db.topics.find({}, { 'id': { "$toString": '$_id' }, 'name': 1, '_id': 0 })))
