from twython import Twython # conda install twython on a console
import sys
sys.path.append('./edtech')

class EdTech(object):
    def __init__(self, keyword, config):
        self.keyword = keyword
        self.config = config
        self.twitter = Twython(config["consumer_key"],config["consumer_secret"],config["access_token"],config["access_token_secret"])

    def get_hastags(self, tweet):
        return [hashtag for hashtag in tweet.split() if hashtag[0] == '#']

    def run(self):
        tweets = self.twitter.search(q=self.keyword, count=5)["statuses"]
        count = 0
        for tweet in tweets:
            tweet_id = tweet["id"] # tweet id
            date = tweet["created_at"] # tweet date
            user = tweet["user"]["screen_name"] # user's screen_name
            bio = tweet["user"]["description"] # user's bio
            text = tweet["text"] # text of the tweet
            user_location = tweet['user']['location']
            geo = tweet['geo']
            retweet_count = tweet['retweet_count']
            created_at = tweet['created_at']
            coords = tweet['coordinates']
            print(coords, geo, user_location)
            count += 1
            # print(tweet['hashtag'])
            print("tweet id: ", tweet_id, "   sent on: ", date, "   tweeted by: @", user, sep="")
            print(text)
        # print(tweets[0].keys())
        print(count, " tweets were crawled")
