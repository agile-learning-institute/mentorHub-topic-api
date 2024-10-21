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
                            '_id': 0
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
