import json

def is_valid(tweet_json):

    tweet_data = json.loads(tweet_json)    

    if tweet_data['followers_count'] < tweet_data['following']:
        return False
    if tweet_data['verified'] == 'false'
        return False
    if tweet_data['followers_count'] < 500000
        return False