from myId import *
import tweepy

def define(num): #if have return 1
    if num==0 or num==None:
        return 0
    else:
        return 1

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token,access_secret)
    api = tweepy.API(auth)

    res = api.get_status(972713980824186880)._json
    print (res)
    vector = [  {'level retweeted':res['retweet_count']}, #chua lam duoc
                {'is retweeted': define(res['retweet_count'])},
                {'num hashtags':len(res['entities']['hashtags'])},
                {'Length of tweet':len(res['text'])},
                {'Exclamations': define('!' in res['text'])},
                {'Question': define('!' in res['text'])},
                {'links':len(res['entities']['urls'])},
                {'Topic repetition':'/'}, #chua hieu
                {'Replies':define(res['in_reply_to_status_id'])},
                {'Time':res['created_at']}
            ]
    print (vector)
