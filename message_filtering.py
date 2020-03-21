
def is_valid(tweet_data):
    valid = False
    try:
        if tweet_data['user']['followers_count'] > tweet_data['user']['following'] and \
                tweet_data['user']['verified'] == 'true' and tweet_data['user']['followers_count'] > 500000:
            valid = True
        return valid
    except:
        return valid



