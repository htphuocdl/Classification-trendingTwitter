from myId import *
import os
from googletrans import Translator
import tweepy
import json

# Make it work for Python 2+3 and with Unicode
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

def process_dir(data_path):
    # get candidates
    lst_input = []
    for filename in os.listdir(data_path):
        if filename.endswith('.txt'):
            lst_input.append(filename)
    return lst_input

def main(data_path):
    lst_input = process_dir(data_path)
    for file in lst_input:
        with open(os.path.join(data_path,file),'r') as f:
            lines = f.readlines()

def isReplies(a):
    if a and a>0:
        return 1
    else:
        return 0

def getDataHashCode(trendingHashCode):
    translator = Translator()
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_secret)
    api = tweepy.API(auth)

    data = {}
    temp=0
    temp1=0
    with open('../../data/tweets/'+trendingHashCode, 'r') as file:
        for line in file:
            print (temp, temp1, line.split()[0])
            temp+=1
            try:
                _id = line.split()[0]
                res = api.get_status(_id)._json
                data[_id] ={    'userId':res['user']['id'],
                                'tweet':res['text'],
                                'retweet_count':res['retweet_count'],
                                'arr_hashtags':res['entities']['hashtags'],
                                'links':len(res['entities']['urls']),
                                'isReplies':isReplies(res['in_reply_to_status_id']),
                                'created':res['created_at'],
                                'lang':res['lang']}
                print ('twitter')
                translator.translate(res['text']).text
                print ('google')
                temp1+=1
            except tweepy.TweepError:
                print ('---------------------')
    #Write JSON file

    str_ = json.dumps(data,
                        indent=4, sort_keys=False,
                        separators=(',', ': '), ensure_ascii=False)
    filename='/home/crazytrau/Desktop/features/'+trendingHashCode+'.json'
    file = open(filename, "w", encoding='utf-8')
    file.write(str_)
    file.close()

# getDataHashCode('cd13f4e6921f58002958a760278a768d')
