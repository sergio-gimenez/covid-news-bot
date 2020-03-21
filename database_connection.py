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

    def find(self, filter):
        cursor = self.news.find(filter)
        return [row for row in cursor]

    def find_by_keyword(self, keyword):
        cursor = self.news.find({'keyword': {'$regex': keyword, '$options':'i'}})
        return [row for row in cursor]

    def find_by_time(self, time_begin):
        filter = {'inserted_at': {'$gte': time_begin}}
        return self.find(filter)

    def update_category(self, category):
        filter = {'category': {'$exists': False}}
        list_to_update = self.find(filter)
        for tweet_no_key in list_to_update:
            id_tweet = {'id': tweet_no_key['id']}
            to_add = {'$set': {'category': category}}
            self.news.update_one(id_tweet, to_add)



if __name__ == "__main__":
    mongo = MongoDB()
    time = datetime(2014, 9, 24, 7, 51)
    algo = mongo.update_category(1)
    print()

