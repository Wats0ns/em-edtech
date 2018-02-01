import pymongo
import sys
import json
import tweepy
sys.path.append('./edtech')

class EdTech(object):
    def __init__(self, keyword, config):
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


    def get_hastags(self, tweet):
        return [hashtag for hashtag in tweet.split() if hashtag[0] == '#']

    def get_max_id(self):
        return self.db.tweets.find_one(sort=[("id", pymongo.DESCENDING)])['id']

    def run(self):
        max_id = self.get_max_id()
        tweets = self.twitter.search(q="edtech", count=100, tweet_mode="extended", extended_tweet="full_text", since_id=max_id)
        # print (tweets)
        # print (tweets[0].keys())
        # sys.exit(0)
        count = 0
        for tweet in tweets:
            tweet_id = tweet.id # tweet id
            date = tweet.created_at # tweet date
            user = tweet.user.screen_name # user's screen_name
            bio = tweet.user.description # user's bio
            text = tweet.full_text # text of the tweet
            user_location = tweet.user.location
            geo = tweet.geo
            retweet_count = tweet.retweet_count
            created_at = tweet.created_at
            coords = tweet.coordinates
            # print(coords, geo, user_location)
            count += 1
            with open('data.json', 'w') as outfile:
                json.dump(tweet._json, outfile)
            # print(tweet.hashtag)
            print("tweet id: ", tweet_id, "   sent on: ", date, "   tweeted by: @", user, sep="")
            print(text)
            # print(tweet.entities)
            print(type(tweet._json))
            target = tweet._json
            target["easy_access_hastags"] = [entity["text"] for entity in tweet.entities["hashtags"]]
            self.db.tweets.insert_one(tweet._json)
        print(count, " tweets were crawled")
