"""
RUNNING PROGRAM;

1-Start Apache Kafka
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties

2-Run kafka_push_listener.py (Start Producer)
PYSPARK_PYTHON=python3 bin/spark-submit kafka_push_listener.py

3-Run kafka_twitter_spark_streaming.py (Start Consumer)
PYSPARK_PYTHON=python3 bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.0 kafka_twitter_spark_streaming.py
"""
from __future__ import division
from collections import Counter
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType
from pyspark.sql import SQLContext
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from googletrans import Translator
from datetime import datetime
from pyspark import sql

import MySQLdb
import json
import re
import nltk
import urllib.request as urllib2
import numpy as np
import pickle
import csv
import os
from pyspark.sql.types import Row

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
t0_original = ''
data = {}
data_tweet_geo = {}
removal_list = ['\\','/',',','(',')','!',':','.']
stop = stopwords.words('english')
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.0 pyspark-shell'
os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
translator = Translator()


def getIntent(x):
    tknzr = TweetTokenizer(reduce_len=True)
    a = tknzr.tokenize(x)
    # # # ##print "Twitter tokens: ", a
    tagged = nltk.pos_tag(a)
    # # # ##print 'Tagged: ', tagged

    y = []
    for x in tagged:
        if x[1] == 'VB':
            return x[0]
        else:
            return 'No Verb Found'
outFile = open('temp1.txt',"w")

timePerVector = 60


# writer.writerow(['depth_retweets','ratio_retweets','hashtags',
#         'length','exclamations','questions',
#         'links','topicRepetition','replies',
#         'spreadVelocity','user_diversity1',
#         'retweeted_user_diversity1','hashtag_diversity1',
#         'language_diversity1','vocabulary_diversity1'])
def saveDataToFile(x):
        x = x.collect()
        #print('xzxzxxxxxxxxxxxxxxxxxxxxzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
        #print(x)
        for data in x:
            outFile.write(data)
        outFile.write('\n')
            # writer.writerow([data[0],data[1]])

def turnIntoVector(x):
    #x = x.collect()
    dataFrame = x.toDF()

def getRDD(x):
    if(x!= None):
        return x

def isReplies(a):
    if a and a>0:
        return 1
    else:
        return 0

numberItem = 0
def increaseBag(key, bag):
    try:
        ##print("-------xxxxxxxxxxxxxx------------" + str(key))
        ##print(bag)
        if str(key) in bag.keys():
            bag[key]+=1
        else:
            bag[key]=1
    except:
        pass


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
cursor = None
#Average number of uses of the trending topic in tweets.
topicRepetition=0
#Average number of tweets that are replies to others
replies=0
#Average number of tweets per second in the trend
spreadVelocity=0

user_diversity=dict()

retweeted_user_diversity=dict()

hashtag_diversity=dict()

language_diversity=dict()

vocabulary_diversity=dict()
timeStart = datetime.now()
timeEnd = datetime.now()

def checkExistFile(filepath):
    if  not os.path.isfile(filepath):
        f= open(filepath,"w+")
        f.close()

import os.path
from pathlib import Path

def loadDataFromFile(trends):
    global timeStart
    global timeEnd
    global numberItem
    global depth_retweets
    global ratio_retweets
    global hashtags
    global length
    global exclamations
    global questions
    global links
    global topicRepetition
    global replies
    global spreadVelocity
    global user_diversity
    global retweeted_user_diversity
    global hashtag_diversity
    global language_diversity
    global vocabulary_diversity

    myFile = Path("trends/" +str(trends) + "/data.txt")
    if(myFile.is_file()):
        f = open("trends/" + str(trends) + "/data.txt", "r")
        #print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx')
        #print(f.readlines()[0] + 'wtf')
        f = open("trends/" + str(trends) +"/data.txt", "r")
        numberItem = int(f.readlines()[0])
        #print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx')
        #print(numberItem)
        f = open("trends/" + str(trends) + "/data.txt", "r")
        ratio_retweets = float(f.readlines()[1])
        f = open("trends/" + str(trends) + "/data.txt", "r")
        hashtags = float(f.readlines()[2])
        f = open("trends/" + str(trends) + "/data.txt", "r")
        length = float(f.readlines()[3])
        f = open("trends/" + str(trends) + "/data.txt", "r")
        exclamations = float(f.readlines()[4])
        f = open("trends/" + str(trends) + "/data.txt", "r")
        questions = float(f.readlines()[5])
        f = open("trends/" + str(trends) + "/data.txt", "r")
        links = float(f.readlines()[6])
        f = open("trends/" + str(trends) + "/data.txt", "r")
        topicRepetition = float(f.readlines()[7])
        f = open("trends/" + str(trends) + "/data.txt", "r")
        replies = float(f.readlines()[8])
        f = open("trends/" + str(trends) + "/data.txt", "r")
        tempTime = f.readlines()[9].replace("\n", "")
        # #print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        # #print(tempTime)
        if (len(tempTime) > 23):
            timeStart = datetime.strptime(tempTime, '%Y-%m-%d %H:%M:%S.%f')
        else:
            #print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
            #print(tempTime)
            timeStart = datetime.strptime(tempTime, '%Y-%m-%d %H:%M:%S')
        f = open("trends/" + str(trends) + "/data.txt", "r")
        tempTime = f.readlines()[10].replace("\n", "")
        # #print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        # #print(tempTime)
        if (len(tempTime) > 23):
            timeStart = datetime.strptime(tempTime, '%Y-%m-%d %H:%M:%S.%f')
        else:

            timeStart = datetime.strptime(tempTime, '%Y-%m-%d %H:%M:%S')

        f.close()

    try:
        user_diversity  = json.load(open("trends/" + str(trends)+ "/user_diversity.txt"))
        retweeted_user_diversity  = json.load(open("trends/" + str(trends)+ "/retweeted_user_diversity.txt"))
        hashtag_diversity  = json.load(open("trends/" + str(trends)+ "/hashtag_diversity.txt"))
        language_diversity  = json.load(open("trends/" + str(trends)+ "/language_diversity.txt"))
        vocabulary_diversity  = json.load(open("trends/" + str(trends)+ "/vocabulary_diversity.txt"))
    except:
        pass




def saveDataToFile(trends):
    #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXSAVESAVESAVESAVESAVESAVESAVESAVESAVESAVESAVESAVESAVESAVESAVESAVESAVESAVE")
    if not os.path.exists("trends/" + str(trends)):
        os.makedirs("trends/" + str(trends))
    checkExistFile("trends/" + str(trends)+ "/data.txt")
    checkExistFile("trends/" + str(trends)+ "/user_diversity.txt")
    checkExistFile("trends/" + str(trends)+ "/retweeted_user_diversity.txt")
    checkExistFile("trends/" + str(trends)+ "/hashtag_diversity.txt")
    checkExistFile("trends/" + str(trends)+ "/language_diversity.txt")
    checkExistFile("trends/" + str(trends)+ "/vocabulary_diversity.txt")
    f = open("trends/" + str(trends)+ "/data.txt", 'w+')
    f.truncate()
    f.write(str(numberItem))
    f.write("\n")
    f.write(str(ratio_retweets))
    f.write("\n")
    f.write(str(hashtags))
    f.write("\n")
    f.write(str(length))
    f.write("\n")
    f.write(str(exclamations))
    f.write("\n")
    f.write(str(questions))
    f.write("\n")
    f.write(str(links))
    f.write("\n")
    f.write(str(topicRepetition))
    f.write("\n")
    f.write(str(replies))
    f.write("\n")
    f.write(str(timeStart))
    f.write("\n")
    f.write(str(timeEnd))
    f.close()
    f = open("trends/" + str(trends)+ "/user_diversity.txt", 'w+')
    f.truncate()
    f.close()
    f = open("trends/" + str(trends)+ "/retweeted_user_diversity.txt", 'w+')
    f.truncate()
    f.close()
    f = open("trends/" + str(trends)+ "/language_diversity.txt", 'w+')
    f.truncate()
    f.close()
    f = open("trends/" + str(trends)+ "/vocabulary_diversity.txt", 'w+')
    f.truncate()
    f.close()
    f = open("trends/" + str(trends)+ "/hashtag_diversity.txt", 'w+')
    f.truncate()
    f.close()
    json.dump(user_diversity, open("trends/" + str(trends)+ "/user_diversity.txt",'w'))
    json.dump(retweeted_user_diversity, open("trends/" + str(trends)+ "/retweeted_user_diversity.txt",'w'))
    json.dump(hashtag_diversity, open("trends/" + str(trends)+ "/hashtag_diversity.txt",'w'))
    json.dump(language_diversity, open("trends/" + str(trends)+ "/language_diversity.txt",'w'))
    json.dump(vocabulary_diversity, open("trends/" + str(trends)+ "/vocabulary_diversity.txt",'w'))




def getIDFromDB(trend, time, tableName):
    global cursor
    trend = trend.replace("\n","")
    sql = "SELECT MAX(ID) FROM %s WHERE TREND = '%s'" % (tableName,trend)
    print(sql)
    sql = sql.encode("utf-8")
    cursor.execute(sql)

    row = cursor.fetchone()
    try:
        print("HKJOPJBNMKJHBNMLKJKNMKLJBNKJKIJHUGFVBJHGVBNJGV" + row[0])
    except:
        pass
    if (getTimeFromDB(row[0], time, tableName) == True):
        return row
    sql = "SELECT MAX(ID) FROM %s"  % (tableName)
    cursor.execute(sql)
    row = cursor.fetchone()
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxxXXXXXX",row[0])
    if(row[0] == None):
        return 0
    return row[0] + 1

from datetime import datetime, date

def getTimeFromDB(ID, timeTweet, tableName):
    global cursor
    global timePerVector
    try:
        sql = "SELECT TIME FROM %s WHERE ID = %s" % (tableName,ID)
        print(sql)
        cursor.execute(sql)
        time = cursor.fetchone()
        time = time[0]
        if(len(time) > 20):
            datetime_object = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        else:
            datetime_object = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        print(timeTweet)
        print(datetime_object)
        timeCpr = abs(timeTweet - datetime_object)

        print("XXXXXXXXXXXXXXXXXXXXXX TIME", timeCpr)
        if(timeCpr.total_seconds() < timePerVector * 60):
            print("XXXXXXXXXXXXXXXXXFALSE CAI BEEP")
            return True
        else:
            print("XXXXXXXXXXXXXXXXXFALSE ")
            return False
    except Exception as e:
        print("XXXXXXXXXXXXXXXXXFALSE FALSE" + str(e))
        return False

def getFeature(x):
    # print("WTFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"+x[1])
    global numberItem
    global timeEnd
    global timeStart
    global depth_retweets
    global ratio_retweets
    global hashtags
    global length
    global exclamations
    global questions
    global links
    global topicRepetition
    global replies
    global spreadVelocity
    global user_diversity
    global retweeted_user_diversity
    global hashtag_diversity
    global language_diversity
    global vocabulary_diversity
    global db
    global cursor
    # print("XXXXXXXXXXXXX")
    # Open database connection
    db = MySQLdb.connect("localhost", "htduongdl96", "motorola", "DBtweet")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    try:

        sql = "use DBtweet"
        cursor.execute(sql)
        sql = """CREATE TABLE ALL_TWEET_VECTOR (
                 ID  INT NOT NULL AUTO_INCREMENT,
                 TREND  CHAR(200) CHARACTER SET utf8 COLLATE utf8_general_ci,
                 TIME VARCHAR(30),
                DEPTH_RETWEETS FLOAT ,
                RATIO_RETWEETS FLOAT ,
                HASHTAGS FLOAT ,
                LENGTH FLOAT ,
                EXCLAMATIONS  FLOAT ,
                QUESTIONS FLOAT ,
                LINKS FLOAT ,
                TOPICREPETITION FLOAT ,
                REPLIES  FLOAT ,
                SPREADVELOCITY  FLOAT ,
                USER_DIVERSITY FLOAT ,
                RETWEETED_USER_DIVERSITY FLOAT ,
                HASHTAG_DIVERSITY FLOAT ,
                LANGUAGE_DIVERSITY FLOAT ,
                VOCABULARY_DIVERSITY FLOAT ,
                CLASS INT,
                CONFIRMED TINYINT(1),
                PRIMARY KEY (ID)
                 )"""
        cursor.execute(sql)
        sql = """CREATE TABLE TWEET_VECTOR_TRAIN (
                ID INT NOT NULL AUTO_INCREMENT,
                 TREND  CHAR(200) CHARACTER SET utf8 COLLATE utf8_general_ci,
                TIME VARCHAR(30),
                DEPTH_RETWEETS FLOAT ,
                RATIO_RETWEETS FLOAT ,
                HASHTAGS FLOAT ,
                LENGTH FLOAT ,
                EXCLAMATIONS  FLOAT ,
                QUESTIONS FLOAT ,
                LINKS FLOAT ,
                TOPICREPETITION FLOAT ,
                REPLIES  FLOAT ,
                SPREADVELOCITY  FLOAT ,
                USER_DIVERSITY FLOAT ,
                RETWEETED_USER_DIVERSITY FLOAT ,
                HASHTAG_DIVERSITY FLOAT ,
                LANGUAGE_DIVERSITY FLOAT ,
                VOCABULARY_DIVERSITY FLOAT ,
                CLASS INT,
                CONFIRMED TINYINT(1),
                PRIMARY KEY (ID)
                 )"""
        cursor.execute(sql)
        sql = """CREATE TABLE DETAIL_TWEET (
                 ID INT NOT NULL AUTO_INCREMENT,
                 ID_TWEET BIGINT,
                 TREND  CHAR(200) CHARACTER SET utf8 COLLATE utf8_general_ci,
                 PRIMARY KEY (ID))"""
        cursor.execute(sql)
    except:
        pass


    #print ('------------' + json.dumps(x, indent = 4) + '----------------')
    res = json.loads(x)
    # #print('asddddddddddddddddddadsada',res['text'])
    print(res)
    # print(res['id'])
    # try:
    #     test = {    'userId':res['user']['id'],
    #                 'tweet': translator.translate(res['text']).text,
    #                 'retweet_count': res['retweet_count'],
    #                 'arr_hashtags': res['entities']['hashtags'],
    #                 'links': len(res['entities']['urls']),
    #                 'isReplies': isReplies(res['in_reply_to_status_id']),
    #                 'created': res['created_at'],
    #                 'lang': res['lang']}
    # except:
    #     return
    #     pass
    trend = checkTrend("trends.txt", res['tweet'])

    if trend == "a":
        return

    timeStartTweet = res['created']
    stringTime = timeStartTweet[4:7] + ' ' + timeStartTweet[8:10] + ' ' + timeStartTweet[-4:] + ' ' + timeStartTweet[11:13] + ':' + timeStartTweet[14:16] + ':' + timeStartTweet[
                                                                                                                17:19]
    ##print(stringTime)
    datetime_object = datetime.strptime(stringTime, '%b %d %Y %H:%M:%S')
    ID = getIDFromDB(trend,datetime_object,"ALL_TWEET_VECTOR")
    # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx" + ID)
    loadDataFromFile(ID)
    numberItem = numberItem + 1

    ###print('------------' + json.dumps(test, indent = 4) + '------------')
    #Return feature
     # 2
    tweetJson = res
    ###print(json.dumps(test, indent = 4))
    ###print (tweetJson)

    if tweetJson['retweet_count']>0 :
        ##print('--------------------------------1-----' + str(depth_retweets))
        depth_retweets=depth_retweets+1
        ##print('--------------------------------1-----' + str(depth_retweets))
    if tweetJson['retweet_count']>0 :
        ##print('--------------------------------2-----' + str(ratio_retweets))
        ratio_retweets=ratio_retweets+1
        ##print('--------------------------------2-----' + str(ratio_retweets))
    hashtags+=len(tweetJson['arr_hashtags'])
    length+=len(tweetJson['tweet'])
    if '!' in tweetJson['tweet']:
        ##print('--------------------------------3-----' + str(exclamations))
        exclamations=exclamations+1
        ##print('--------------------------------3-----' + str(exclamations))
    if '?' in tweetJson['tweet']:
        ##print('--------------------------------4-----' + str(questions))
        questions=questions+1
        ##print('--------------------------------4-----' + str(questions))
    links+=tweetJson['links']
    ##print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"+ str(tweetJson['userId']))
    topicRepetition += tweetJson['tweet'].lower().count(trend.lower().replace("#",""))
    if tweetJson['isReplies']>0:
        replies+=1
    increaseBag(tweetJson['userId'], user_diversity)
    if tweetJson['retweet_count']>0:
        increaseBag(tweetJson['userId'], retweeted_user_diversity)
    for hashtag in tweetJson['arr_hashtags']:
        increaseBag(hashtag['text'], hashtag_diversity)
    increaseBag(tweetJson['lang'], language_diversity)
    print("12313132")
    try:
        tweetJson['tweet'] = translator.translate(tweetJson['tweet']).text
    except:
        pass
    print("1312444123")
    newBag = [w.lower() for w in tweetJson['tweet'].split()]
    if len(newBag)>0:
        for word in newBag:
            increaseBag(word, vocabulary_diversity)
    time = tweetJson['created']
    #Sun Apr 29 11:03:32 +0000 2018
    #print("####################################################################")
    #print(time)
    ##print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    ##print(time)
    stringTime = time[4:7]+' '+time[8:10]+' '+time[-4:]+' '+time[11:13]+':'+time[14:16]+':'+time[17:19]
    ##print(stringTime)
    datetime_object = datetime.strptime(stringTime, '%b %d %Y %H:%M:%S')
    if datetime_object > timeEnd:
        timeEnd = datetime_object
    if datetime_object < timeStart:
        timeStart = datetime_object

    ##print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" + stringTime)
    spreadVelocity = timeEnd - timeStart

    depth_retweets= depth_retweets/numberItem
    ratio_retweets= ratio_retweets/numberItem
    hashtags= hashtags/numberItem
    length= length/numberItem
    exclamations= exclamations/numberItem
    questions= questions/numberItem
    links= links/numberItem
    ##print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    topicRepetition= topicRepetition/numberItem
    replies= replies/numberItem
    spreadVelocity= spreadVelocity.total_seconds()/numberItem
    user_diversity1= calShannon(user_diversity)
    retweeted_user_diversity1= calShannon(retweeted_user_diversity)
    hashtag_diversity1= calShannon(hashtag_diversity)
    language_diversity1= calShannon(language_diversity)
    vocabulary_diversity1= calShannon(vocabulary_diversity)

    sql = "INSERT INTO DETAIL_TWEET(ID_TWEET,TREND) VALUES (%d, '%s')" % (int(res["id"]), trend)
    sql.encode('utf-8')
    print(sql)
    try:
        cursor.execute(sql)
    except:
        pass
    #print ("OMGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG" + str(cursor.lastrowid))

    ##print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    vector = []

    vector.append(depth_retweets)
    vector.append(ratio_retweets)
    vector.append(hashtags)
    vector.append(length)
    vector.append(exclamations)
    vector.append(questions)
    vector.append(links)
    vector.append(topicRepetition)
    vector.append(replies)
    vector.append(spreadVelocity)
    vector.append(user_diversity1)
    vector.append(retweeted_user_diversity1)
    vector.append(hashtag_diversity1)
    vector.append(language_diversity1)
    vector.append(vocabulary_diversity1)

    print(trend)
    if numberItem > 50:
        Class = predictTrend(vector,trend,timeStart)
    else:
        Class = -1
    addNewTrend("ALL_TWEET_VECTOR",trend,depth_retweets,ratio_retweets,hashtags,
            length,exclamations,questions,
            links,topicRepetition,replies,
            spreadVelocity,user_diversity1,
            retweeted_user_diversity1,hashtag_diversity1,
            language_diversity1,vocabulary_diversity1,Class, timeStart)
    saveDataToFile(ID)
    return [str(depth_retweets),str(ratio_retweets),str(hashtags),
            str(length),str(exclamations),str(questions),
            str(links),str(topicRepetition),str(replies),
            str(spreadVelocity),str(user_diversity1),
            str(retweeted_user_diversity1),str(hashtag_diversity1),
            str(language_diversity1),str(vocabulary_diversity1)]
    #return [str(), str(), ]

def exportModel(model,filename):
    pickle.dump(model,open(filename,'wb'))

def importModel(filename):
    with open(filename, 'rb') as fin:
        classifier = pickle.load(fin)
        return classifier

#check that input belong to any trend:

def addNewTrend(TableName, trend,depth_retweets,ratio_retweets,hashtags,
            length,exclamations,questions,
            links,topicRepetition,replies,
            spreadVelocity,user_diversity,
            retweeted_user_diversity,hashtag_diversity,
            language_diversity,vocabulary_diversity,Class, time):


    if(getTimeFromDB(getIDFromDB(trend,time,TableName),time,TableName) == False):
        sql = "INSERT INTO %s(\
TREND, DEPTH_RETWEETS, RATIO_RETWEETS, HASHTAGS,\
LENGTH, EXCLAMATIONS, QUESTIONS,LINKS  ,TOPICREPETITION , REPLIES,\
SPREADVELOCITY   ,USER_DIVERSITY  ,RETWEETED_USER_DIVERSITY  ,HASHTAG_DIVERSITY ,\
LANGUAGE_DIVERSITY, VOCABULARY_DIVERSITY, CLASS, TIME)"\
 "VALUES ('%s', %f, %f,\n %f,\
%f, %f, %f, %f, %f, %f, \
%f, %f, %f, %f, \
%f, %f, %d, '%s');" % \
              (TableName, trend.rstrip(), depth_retweets, ratio_retweets, hashtags,
               length, exclamations, questions,
               links, topicRepetition, replies,
               spreadVelocity, user_diversity,
               retweeted_user_diversity, hashtag_diversity,
               language_diversity, vocabulary_diversity, Class, time)
        print(sql)
        sql = sql.encode("utf-8")
        cursor.execute(sql)
        db.commit()
    else:
        updateTrend(TableName,getIDFromDB(trend,time,TableName), depth_retweets,ratio_retweets,hashtags,
            length,exclamations,questions,
            links,topicRepetition,replies,
            spreadVelocity,user_diversity,
            retweeted_user_diversity,hashtag_diversity,
            language_diversity,vocabulary_diversity,Class)


def updateTrend(TableName,ID,depth_retweets,ratio_retweets,hashtags,
            length,exclamations,questions,
            links,topicRepetition,replies,
            spreadVelocity,user_diversity,
            retweeted_user_diversity,hashtag_diversity,
            language_diversity,vocabulary_diversity,Class):
    sql = "Update %s" \
" set DEPTH_RETWEETS = %f,RATIO_RETWEETS= %f,HASHTAGS= %f, \
LENGTH= %f, EXCLAMATIONS= %f, QUESTIONS = %f,LINKS = %f ,TOPICREPETITION = %f ,REPLIES = %f  ,\
SPREADVELOCITY  = %f ,USER_DIVERSITY = %f ,RETWEETED_USER_DIVERSITY = %f ,HASHTAG_DIVERSITY = %f,\
LANGUAGE_DIVERSITY= %f, VOCABULARY_DIVERSITY= %f, CLASS = %d " \
"WHERE ID = %d;" \
          % (TableName, depth_retweets, ratio_retweets, hashtags,
             length, exclamations, questions,
             links, topicRepetition, replies,
             spreadVelocity, user_diversity,
             retweeted_user_diversity, hashtag_diversity,
             language_diversity, vocabulary_diversity,Class, ID[0])
    print(sql)
    sql = sql.encode("utf-8")
    cursor.execute(sql)
    db.commit()

def updateTrendClass(TableName,ID,Class):
    sql = "Update %s" \
          "set CLASS = %d" \
          "WHERE ID = %d" \
          % (TableName, Class, ID)
    cursor.execute(sql)
    db.commit()

def checkTrend(filename, input):
    f = open(filename,"r", encoding='utf-8')
    # #print(input)
    #print("AAAAAA")
    for i in f:
        if i.replace("#","").rstrip() in input:
            # #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" + i)
            return i
            break
    return "a"

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
def predictTrend(vector,trend, timeStart):
    classifier = importModel("model.pkl")
    # sc = StandardScaler()
    # vector = sc.transform(vector)
    # print("DMJMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM" + str(vector))

    test = [vector[0], vector[1], vector[2], vector[3],vector[4], vector[5], vector[6], vector[7], vector[8]
        , vector[9], vector[10], vector[11], vector[12], vector[13], vector[14]]
    class_probabilities = classifier.predict_proba([test])

    CLASS = classifier.predict([test])[0]


    print("CHO PHUOC XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",(class_probabilities.max(1)))

    bagOfWordClassifier = importModel("SVM_BagofWords.pkl")
    
    count_vect = CountVectorizer()
    if(class_probabilities.max(1)[0] > 0.8):
        if(numberItem > 50):
            addNewTrend("ALL_TWEET_VECTOR", trend, vector[0], vector[1], vector[2], vector[3],vector[4], vector[5], vector[6], vector[7], vector[8]
        , vector[9], vector[10], vector[11], vector[12], vector[13], vector[14], CLASS, timeStart)
    else:
        sql = ""

    # print(classifier.predict([test]))

    return CLASS


def forEachBatch(x):
    tweet = x[1].split("\n")
    for i in tweet:
        try:
            getFeature(i)
            i = 0
        except:
            pass



if __name__ == "__main__":
    try:
        #Create Spark Context to Connect Spark Cluster
        sc = SparkContext(appName="PythonStreamingKafkaTweetCount")

        #Set the Batch Interval is 2 sec of Streaming Context
        ssc = StreamingContext(sc, 2)
        # sqlContext = sql.SQLContext(sc)
        #Create Kafka Stream to Consume Data Comes From Twitter Topic
        #localhost:2181 = Default Zookeeper Consumer Address
        kafkaStream = KafkaUtils.createStream(ssc, 'localhost:2181', 'spark-streaming', {'twitter':1})
        #Parse Twitter Data as json
        parsed = kafkaStream.map(lambda v: forEachBatch(v))
        #parsed = kafkaStream.map(lambda x: x[1])
        #kafkaStream.saveAsTextFiles('test.txt')
        #Count the number of tweets per Usere
        #lines = parsed.map(lambda x: x[1])
        # tweets = parsed.map(getFeature)
        # ##print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        #print('asdljaslkdjaslkjdasjdlkajdlasjkd',len(tweets))
        parsed.pprint()
        #tweets.saveDataToFile("1")
        # vector = np.array(tweets)
        #rdd = tweets.foreachRDD(getRDD)
        #turnIntoVector(rdd)
        # ##print(vector)

        #Start Execution of Streams

        ssc.start()
        ssc.awaitTermination()
    except:
        pass
