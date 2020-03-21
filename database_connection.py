import pymongo
import dns
from Constants import Constants


class MongoDB:
    def __init__(self):
        self.db_client = pymongo.MongoClient(Constants.MONGODB_URL)
        self.news = self.db_client.covid.news
        self.test = self.db_client.covid.testing

    def insert_one(self, dict_to_insert):
        self.news.insert_one(dict_to_insert)

    def find_by_time(self, time_begin):
        self.news.find({"inserted_at"})



if __name__=="__main__":
    mongo = MongoDB()
    mongo.insert_one({'name':'pepe'})

