import os
import tweepy

# authenticate
API_KEY = ""
API_SECRET = ""
ACCESS_TOKEN = ""
TOKEN_SECRET = ""

twitter_oauth = tweepy.OAuthHandler(API_KEY, API_SECRET)
twitter_oauth.set_access_token(ACCESS_TOKEN, TOKEN_SECRET)

twitter_api = tweepy.API(twitter_oauth)
bot_id = twitter_api.verify_credentials().id

try:
    twitter_api.verify_credentials()
    print("Logged in")
except tweepy.TweepError as e:
    print(e)
except Exception as e:
    print(e)
    
# create stream
class StreamListener(tweepy.StreamListener):
  def on_status(self, status):
    if status.in_reply_to_status_id is not None or status.user.id == bot_id:
      return
      
    if not status.retweeted:
      try:
        tweet_to_quote_url="https://twitter.com/" + status.user.screen_name + "/status/" + str(status.id)
        twitter_api.update_status("message", attachment_url=tweet_to_quote_url)        
        print("RTed successfully")
      except Exception as e:
        print(e)
              
  def on_error(self, status):
    print(f"RTing error: {status}")
    
tweets_listener = StreamListener(twitter_api)
tweet_stream = tweepy.Stream(twitter_api.auth, tweets_listener)
tweet_stream.filter(track=["#hashtag1", "hashtag2"])