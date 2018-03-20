#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 13:55:03 2018

@author: crazytrau
"""

# generate vector feature

import json
import numpy as np
from pprint import pprint
from datetime import datetime

topicName = 'Rich Eisen'.lower()

data = json.load(open('output.json'))

vector = {    'depth_retweets':0,
              'ratio_retweets':0,
              'hashtags':0,
              'length':0,
              'exclamations':0,
              'questions':0,
              'links':0,
              'topicRepetition':0,
              'replies':0,
              'spreadVelocity':1,
              'user_diversity':0,
              'retweeted_user_diversity':0,
              'hashtag_diversity':0,
              'language_diversity':0,
              'vocabulary_diversity':0}
numberItem = len(data)
def increaseBag(key, bag):
    if key in bag.keys():
        bag[key]+=1
    else:
        bag[key]=1    

def calShannon(bag):
    sum=0
    for item in bag:
        temp = bag[item]/ numberItem
        sum += temp*np.log(temp)
    return -1*sum
#Average number of retweet levels in tweets.
depth_retweets=0
#Ratio of tweets that contain a retweet.
ratio_retweets=0
#Average number of hashtags in tweets.
hashtags=0
#Average length of tweets
length=0
#Number of tweets with exclamation signs.
exclamations=0
#Number of question signs in tweets.
questions=0
#Average number of links in tweets
links=0
#Average number of uses of the trending topic in tweets. 
topicRepetition=0
#Average number of tweets that are replies to others
replies=0
#Average number of tweets per second in the trend
spreadVelocity=0 # 2
#Shannon’s diversity index of users who posted tweets
user_diversity={}
#Shannon’s diversity index of users who were retweeted in the trend (not the user who retweets).
retweeted_user_diversity={}
#Shannon’s diversity index of hashtags included in the trend.
hashtag_diversity={}
#Shannon’s diversity index of languages used in the trend.
language_diversity={}
#Shannon’s diversity index of terms contained in the trend.
vocabulary_diversity={}

#every json tweet
for tweetJson in data:
    tweetJson = data[tweetJson]
    #print (tweetJson)
    if tweetJson['retweet_count']>0 : depth_retweets+=1
    if tweetJson['retweet_count']>0 : ratio_retweets+=1
    hashtags+=len(tweetJson['arr_hashtags'])
    length+=len(tweetJson['tweet'])
    if '!' in tweetJson['tweet']: exclamations+=1
    if '?' in tweetJson['tweet']: questions+=1
    links+=tweetJson['links']
    topicRepetition += tweetJson['tweet'].lower().count(topicName)
    if tweetJson['isReplies']>0:replies+=1
    #time = tweetJson['created']
    #stringTime = time[4:7]+' '+time[8:10]+' '+time[-4:]+' '+time[11:13]+':'+time[14:16]+':'+time[17:19]
    #print (stringTime)
    #datetime_object = datetime.strptime(stringTime, '%b %d %Y %H:%M:%S')
    #print (datetime_object)
    increaseBag(tweetJson['userId'], user_diversity)
    if tweetJson['retweet_count']>0: 
        increaseBag(tweetJson['userId'], retweeted_user_diversity)
        
    for hashtag in tweetJson['arr_hashtags']:
        increaseBag(hashtag['text'], hashtag_diversity)
    increaseBag(tweetJson['lang'], language_diversity)
    newBag = [w.lower() for w in tweetJson['tweet'].split()]
    if len(newBag)>0:
        for word in newBag:
            increaseBag(word, vocabulary_diversity)

#Average number of tweets per second in the trend
time = data[next(iter(data))]['created']
stringTime = time[4:7]+' '+time[8:10]+' '+time[-4:]+' '+time[11:13]+':'+time[14:16]+':'+time[17:19]
datetime_objectBegin = datetime.strptime(stringTime, '%b %d %Y %H:%M:%S')

temp = data.popitem()
time = temp[1]['created'] 
stringTime = time[4:7]+' '+time[8:10]+' '+time[-4:]+' '+time[11:13]+':'+time[14:16]+':'+time[17:19]
datetime_objectEnd = datetime.strptime(stringTime, '%b %d %Y %H:%M:%S')

spreadVelocity = datetime_objectEnd - datetime_objectBegin 
spreadVelocity.total_seconds()

#fill value to vector
vector['depth_retweets']= depth_retweets/numberItem
vector['ratio_retweets']= ratio_retweets/numberItem
vector['hashtags']= hashtags/numberItem
vector['length']= length/numberItem
vector['exclamations']= exclamations/numberItem
vector['questions']= questions/numberItem
vector['links']= links/numberItem
vector['topicRepetition']= topicRepetition/numberItem
vector['replies']= replies/numberItem
vector['spreadVelocity']= spreadVelocity/numberItem
vector['user_diversity']= calShannon(user_diversity)
vector['retweeted_user_diversity']= calShannon(retweeted_user_diversity)
vector['hashtag_diversity']= calShannon(hashtag_diversity)
vector['language_diversity']= calShannon(language_diversity)
vector['vocabulary_diversity']= calShannon(vocabulary_diversity)

print (vector)
