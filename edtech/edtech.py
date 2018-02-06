import pymongo
import sys
import json
import tweepy
sys.path.append('./edtech')
from tweet import Tweet

class EdTech(object):
    def __init__(self, keyword, config, logging):
        self.keyword = keyword
        self.config = config
        # self.twitter = Twython(config.twitter["consumer_key"],config.twitter["consumer_secret"],config.twitter["access_token"],config.twitter["access_token_secret"])
        auth = tweepy.OAuthHandler(config.twitter["consumer_key"], config.twitter["consumer_secret"])

        auth.set_access_token(config.twitter['access_token'], config.twitter['access_token_secret'])
        self.twitter = tweepy.API(auth)
        self.mongo = pymongo.MongoClient(config.mongo['host'],
                                username=config.mongo['username'],
                                password=config.mongo['password'])
        self.db = self.mongo.edtech
        self.logging = logging
        self.logging.debug('START: Connected to {username}@{host}'.format(host=config.mongo['host'], username=config.mongo['username']))

    def get_max_id(self):
        return self.db.tweets.find_one(sort=[("id", pymongo.DESCENDING)])['id']

    def get_search(self, query, count, max_id):
        print('Looking for: {query} since {max_id}'.format(query=query, max_id=max_id))
        return self.twitter.search(q=query, count=count, tweet_mode="extended", extended_tweet="full_text", since_id=max_id)

    def run(self):
        raise ValueError
        max_id = self.get_max_id()
        tweets = self.get_search(self.keyword, 10, max_id)
        count = 0
        while (len(tweets) > 0):
            for tweet in tweets:
                item = Tweet(tweet)
                count += 1
                # with open('data.json', 'w') as outfile:
                #     json.dump(tweet._json, outfile)
                item_ready = item.format_save()
                self.db.tweets.update({'id': item_ready['id']}, item_ready, upsert=True)
            max_id = self.get_max_id()
            tweets = self.get_search(self.keyword, 10, max_id)
        self.logging.debug('END: {nb} tweets were crawled'.format(nb=count))
        print(count, " tweets were crawled")
