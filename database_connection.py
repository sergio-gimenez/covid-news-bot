import pymongo
import dns
from Constants import Constants
from datetime import datetime


class MongoDB:
    def __init__(self):
        self.db_client = pymongo.MongoClient(Constants.MONGODB_URL)
        self.news = self.db_client.covid.news
        self.test = self.db_client.covid.testing

    def insert_one(self, dict_to_insert):
        self.news.insert_one(dict_to_insert)

    def find_by_time(self, time_begin):
        cursor = self.news.find({'inserted_at': {'$gte': time_begin}})
        return [row for row in cursor]


if __name__=="__main__":
    mongo = MongoDB()
    time = datetime(2014, 9, 24, 7, 51)
    algo = mongo.find_by_time(time)
    print()

