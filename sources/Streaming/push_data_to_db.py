import json
import csv
from datetime import datetime
import numpy as np
import MySQLdb
def generateFeature(topicName, filename, label):

    data = json.load(open(filename))
    numberItem = len(data)
    if (numberItem <= 0):
        return None
    vector =[]
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
        topicRepetition += tweetJson['tweet'].lower().count(topicName.lower())
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

    spreadVelocity =   datetime_objectBegin - datetime_objectEnd
    #fill value to vector
    vector.append(depth_retweets/numberItem)
    vector.append(ratio_retweets/numberItem)
    vector.append(hashtags/numberItem)
    vector.append(length/numberItem)
    vector.append(exclamations/numberItem)
    vector.append(questions/numberItem)
    vector.append(links/numberItem)
    vector.append(topicRepetition/numberItem)
    vector.append(replies/numberItem)
    if spreadVelocity.total_seconds() > 0:
        vector.append(numberItem/spreadVelocity.total_seconds())
    else:
        vector.append(0)
    vector.append(calShannon(user_diversity))
    vector.append(calShannon(retweeted_user_diversity))
    vector.append(calShannon(hashtag_diversity))
    vector.append(calShannon(language_diversity))
    vector.append(calShannon(vocabulary_diversity))
    if label =='ongoing-event':
        vector.append(0)
    elif label =='news':
        vector.append(1)
    elif label =='meme':
        vector.append(2)
    elif label =='commemorative':
        vector.append(3)
    return vector


arrVectors = []

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
    # cursor.execute(sql)
    cursor.execute(sql)
    sql = """CREATE TABLE DETAIL_TWEET (
             ID INT NOT NULL,
             ID_TWEET INT)"""
    cursor.execute(sql)
except:
    pass


with open('TT-annotations.csv', newline='', encoding="utf8") as csvfile:
    trendingTopicArr = csv.reader(csvfile, delimiter=';')
    i = 0
    db.set_character_set('utf8mb4')
    for trendingTopic in trendingTopicArr:
        path = '../features/' + trendingTopic[0] + '.json'
        temp = generateFeature(trendingTopic[2], path, trendingTopic[3])
        #            print(trendingTopic[3])
        if temp != None:
            arrVectors.append(temp)
            print (arrVectors[i])
            trends = trendingTopic[2]
            print(trends)
            sql = "INSERT INTO TWEET_VECTOR_TRAIN(\
                       TREND, DEPTH_RETWEETS,RATIO_RETWEETS,HASHTAGS, \
                        LENGTH, EXCLAMATIONS, QUESTIONS,LINKS  ,TOPICREPETITION  ,REPLIES   ,\
                        SPREADVELOCITY   ,USER_DIVERSITY  ,RETWEETED_USER_DIVERSITY  ,HASHTAG_DIVERSITY ,\
                        LANGUAGE_DIVERSITY, VOCABULARY_DIVERSITY, CLASS)\
                       VALUES ('%s', %f, %f, %f,\
                        %f, %f, %f,%f, %f, %f," \
                  "%f, %f, %f, %f, \
                   %f, %f, %d)" % \
                  (trends, arrVectors[i][0], arrVectors[i][1], arrVectors[i][2],
                   arrVectors[i][3], arrVectors[i][4], arrVectors[i][5],
                   arrVectors[i][6], arrVectors[i][7], arrVectors[i][8],
                   arrVectors[i][9], arrVectors[i][10],
                   arrVectors[i][11], arrVectors[i][12],
                   arrVectors[i][13], arrVectors[i][14], arrVectors[i][15])
            cursor.execute(sql)
            db.commit()
            i = i + 1