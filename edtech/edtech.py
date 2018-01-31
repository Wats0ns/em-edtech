from twython import Twython # conda install twython on a console
import sys
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

    def get_hastags(self, tweet):
        return [hashtag for hashtag in tweet.split() if hashtag[0] == '#']

    def run(self):
        tweets = self.twitter.search(q="macron", count=1, tweet_mode="extended", extended_tweet="full_text")
        print (tweets[0])
        print (dir(tweets[0]))
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
            print(coords, geo, user_location)
            count += 1
            # print(tweet.hashtag)
            print("tweet id: ", tweet_id, "   sent on: ", date, "   tweeted by: @", user, sep="")
            print(text)
            print(tweet.truncated)
        print(count, " tweets were crawled")
