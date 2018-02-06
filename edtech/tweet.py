class Tweet:

    def __init__(self, tweet):
        self.json = tweet._json
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
        print("tweet id: ", tweet_id, "   sent on: ", date, "   tweeted by: @", user, sep="")
        print(text)
        # Formatting the hastags by making them accessible at a higher level
        self.json["easy_access_hastags"] = self.extract_hashtags(tweet)

    @staticmethod
    def extract_hashtags(tweet):
        return [entity["text"] for entity in tweet.entities["hashtags"]]

    def format_save(self):
        return self.json
