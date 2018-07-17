import pykafka
import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import twitter_config
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from urllib3.exceptions import ProtocolError, IncompleteRead
import json
from googletrans import Translator
translator = Translator()
#TWITTER API CONFIGURATIONS
consumer_key = twitter_config.consumer_key
consumer_secret = twitter_config.consumer_secret
access_token = twitter_config.access_token
access_secret = twitter_config.access_secret

#TWITTER API AUTH
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
tweetbatch = []
isRunning = False
import time

def isReplies(a):
    if a and a>0:
        return 1
    else:
        return 0

def StartStream():

	while True:
		try:
			with open("trends.txt", 'r') as f:
				trends = [line.replace("\n","") for line in f]
			if twitter_stream.running is True:
				twitter_stream.disconnect()
			print(trends)
			twitter_stream.filter(track=trends,stall_warnings=True, async=True)
			time.sleep(120)
		except ProtocolError:
			continue
		except IncompleteRead:
			continue
		except:
			continue

#Twitter Stream Listener
class KafkaPushListener(StreamListener):
	def __init__(self):
		#localhost:9092 = Default Zookeeper Producer Host and Port Adresses
		self.client = pykafka.KafkaClient("localhost:9092")

		#Get Producer that has topic name is Twitter
		self.producer = self.client.topics[bytes("twitter", "ascii")].get_producer()

	def on_data(self, data):
		global isRunning
		isRunning = True
		#Producer produces data for consumer
		#Data comes from Twitter
		# print(data)
		# a = json.dumps(data, indent=4)
		# print(a)
		res = json.loads(data)
		# print(res)
		try:
			# print("1")

			test = {'userId': res['user']['id'],
					'id' : res['id'],
					'tweet': res['text'],
					'retweet_count': res['retweet_count'],
					'arr_hashtags': res['entities']['hashtags'],
					'links': len(res['entities']['urls']),
					'isReplies': isReplies(res['in_reply_to_status_id']),
					'created': res['created_at'],
					'lang': res['lang']}
			# print("2")
		except Exception as e:
			print(e)
			return
			pass
		# print(test)
		tweetbatch.append(test)
		print(len(tweetbatch))
		if(len(tweetbatch) >= 100):
			byteSent = ""
			for i in tweetbatch:
				byteSent += json.dumps(i)
				byteSent += "\n"
			# print(byteSent)
			self.producer.produce(bytes(byteSent, "utf-8"))
			tweetbatch.clear()

		return True

	def on_error(self, status):
		global isRunning
		isRunning = False
		print(status)
		time.sleep(60)
		print("WTF")
		return True

#Twitter Stream Config
twitter_stream = Stream(auth, KafkaPushListener())

from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()
sched.start()

def some_job():
	api = tweepy.API(auth)
	trends1 = api.trends_place(1)
	trends = set([trend['name'] for trend in trends1[0]['trends']])
	print(trends)
	if(len(trends) > 10):
		file = open("trends.txt", "w")
		file.flush()
		for i in trends:
			string = i.replace('"', '') + "\n"
			# string = string.encode('utf-8')
			# print(string)
			file = open("trends.txt", "a+")
			file.write(string)
			file.close()


sched.add_job(some_job, 'interval', minutes = 10)




StartStream()

# for e in trends:
# 	print('trends: --------------    ' + e)
# 	twitter_stream.filter(track=[e])z
# 	break
