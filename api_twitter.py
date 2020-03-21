import json
import socket

import pymongo
import dns


from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# Set up your credentials
consumer_key = 'gRD2nikdYfdHyK293wFSQypDA'
consumer_secret = 'IYjjnsG2e7Y4gwDRjXfoEiXvn8UeoTewldBBbD1AEOnuO4q2BD'
access_token = '798809735067635712-VjJvnmpYDGAgD0biq1VGGshoXCVzeX1'
access_secret = 'dYGQJmVCmXXMTyNiOlWFqJGc0F0jhWb1SmlG4HAqCZBNp'


class TweetsListener(StreamListener):

    def __init__(self, csocket):
        super().__init__()
        self.client_socket = csocket


    def on_data(self, data):
        try:
            msg = json.loads(data)
            print(msg)
            print(msg['text'].encode('utf-8'))
            self.client_socket.send(msg['text'].encode('utf-8'))
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


def send_data(c_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track=['codiv', 'coronavirus'])


if __name__ == "__main__":
    s = socket.socket()  # Create a socket object
    host = "127.0.0.1"  # Get local machine name
    port = 5555  # Reserve a port for your service.
    s.bind((host, port))  # Bind to the port

    client = pymongo.MongoClient("mongodb+srv://covid:123123123!@cluster0-juygf.mongodb.net/test?retryWrites=true&w=majority")
    print(client.test)
    print("Listening on port: %s" % str(port))

    s.listen(5)  # Now wait for client connection.
    c, addr = s.accept()  # Establish connection with client.

    print("Received request from: " + str(addr))

    send_data(c)
