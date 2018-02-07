import pymongo
import sys
import json
import tweepy
from multiprocessing.dummy import Pool as ThreadPool
from itertools import repeat
sys.path.append('./edtech')
from tweet import Tweet

class EdTech(object):
    def __init__(self, keywords, config, logging):
        self.keywords = keywords
        self.config = config

        # Twitter part authentification. See tweepy API for more informations
        auth = tweepy.OAuthHandler(config.twitter["consumer_key"], config.twitter["consumer_secret"])
        auth.set_access_token(config.twitter['access_token'], config.twitter['access_token_secret'])
        self.twitter = tweepy.API(auth)

        # PyMongo part, see PyMongo API for more informations
        self.mongo = pymongo.MongoClient(config.mongo['host'],
                                username=config.mongo['username'],
                                password=config.mongo['password'])
        self.db = self.mongo.edtech

        # Logging part
        self.logging = logging
        self.logging.debug('START: Connected to {username}@{host}'.format(host=config.mongo['host'], username=config.mongo['username']))

    def get_max_id(self):
        return self.db.tweets.find_one(sort=[("id", pymongo.DESCENDING)])['id']

    def get_search(self, query, count, max_id):
        print('Looking for: {query} since {max_id}'.format(query=query, max_id=max_id))
        return self.twitter.search(q=query, count=count, tweet_mode="extended", extended_tweet="full_text", since_id=max_id)

    def refresher(self, item):
        del item["_id"]
        tweet = Tweet(item.copy())
        item = tweet.format_save()
        print ("Updated tweet {id}".format(id=item["id"]))
        return self.save_tweet(item)

    def refresh(self):
        """
        This function is used to refresh the data in DB when the content has been changed
        """
        pool = ThreadPool(6)
        tweets = self.db.tweets.find({})
        return pool.map(self.refresher, tweets)


    def save_tweet(self, item):
        return self.db.tweets.update({'id': item['id']}, item, upsert=True)

    def run(self):
        max_id = self.get_max_id()
        count = 0
        for keyword in self.keywords:
            while True:
                max_id = self.get_max_id()
                tweets = self.get_search(keyword, 10, max_id)
                if not len(tweets):
                    self.logging.debug('INFO: no new tweets for {keyword}'.format(keyword=keyword))
                    break
                for tweet in tweets:
                    item = Tweet(tweet._json)
                    count += 1
                    item_ready = item.format_save()
                    with open('data.json', 'w') as outfile:
                        json.dump(item_ready, outfile)
                        sys.exit(0)
                    self.save_tweet(item_ready)
        self.logging.debug('END: {nb} tweets were crawled'.format(nb=count))
        print(count, " tweets were crawled")
