import requests

class Tweet:

    def __init__(self, tweet):
        self.json = tweet
        tweet_id = tweet["id"] # tweet id
        date = tweet["created_at"] # tweet date
        user = tweet["user"]["screen_name"] # user's screen_name
        bio = tweet["user"]["description"] # user's bio
        text = tweet["full_text"] # text of the tweet
        user_location = tweet["user"]["location"]
        geo = tweet["geo"]
        retweet_count = tweet["retweet_count"]
        created_at = tweet["created_at"]
        coords = tweet["coordinates"]
        print("tweet id: ", tweet_id, "   sent on: ", date, "   tweeted by: @", user, sep="")
        print(text)
        # Formatting the hastags by making them accessible at a higher level
        self.json["easy_access_hastags"] = self.extract_hashtags(tweet)
        self.json["easy_access_users"] = self.extract_users(tweet)
        self.json["easy_access_urls"] = self.extract_urls(tweet)
        self.json["easy_access_domains"] = self.extract_domains(self.json["easy_access_urls"])

    @staticmethod
    def extract_hashtags(tweet):
        return list(set([entity["text"].lower() for entity in tweet["entities"]["hashtags"]]))

    @staticmethod
    def extract_users(tweet):
        users = [entity for entity in tweet["entities"]["user_mentions"]]
        users.append({"id": int(tweet["user"]["id_str"]), "name": tweet["user"]["name"], "screen_name": tweet["user"]["screen_name"]})
        return list(users)

    @staticmethod
    def extract_urls(tweet):
        urls = [entity["url"] for entity in tweet["entities"]["urls"]]
        for index, url in enumerate(urls):
            # Nearly all links come from url shortener, so we need to resolve them
            try:
                r = requests.request("HEAD", url)
                urls[index] = r.url
            except requests.exceptions.RequestException as e:
                print(e)
                # We ignore this as there is a lot of tweets with broken redirect
                pass
        return list(set(urls))

    @staticmethod
    def extract_domains(urls):
        domains = []
        for url in urls:
            if url.find('://') != -1:
                url = url[url.find('://') + 3:]
            if url.find('/') != -1:
                url = url[:url.find('/')]
            domains.append(url)
        return domains

    def format_save(self):
        return self.json
