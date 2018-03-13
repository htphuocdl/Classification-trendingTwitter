from myId import *
from googletrans import Translator
import tweepy
import csv

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

if __name__ == "__main__":
    translator = Translator()
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_secret)
    api = tweepy.API(auth)

    with open('output.csv','w',newline='') as csvfile:
        fieldnames = ['tweetId','userId','tweet','retweet_count','arr_hashtags','links','isReplies','created','lang']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames,delimiter='\t')
        writer.writeheader()

        with open('../../../TT-classification/tweets/0a14dee099e100e8bf356a9937a6f974', 'r') as file:
            for line in file:
                print (line.split()[0])
                try:
                    _id = line.split()[0]
                    res = api.get_status(_id)._json
                    writer.writerow({   'tweetId':line.split()[0],
                                        'userId':res['user']['id'],
                                        'tweet':translator.translate(res['text']).text,
                                        'retweet_count':res['retweet_count'],
                                        'arr_hashtags':res['entities']['hashtags'],
                                        'links':len(res['entities']['urls']),
                                        'isReplies':isReplies(res['in_reply_to_status_id']),
                                        'created':res['created_at'],
                                        'lang':res['lang']})
                except tweepy.TweepError:
                    print ('---------------------')
# auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
# auth.set_access_token(access_token,access_secret)
# api = tweepy.API(auth)
# try:
#     res = api.get_status(42659021370568704)
# except tweepy.TweepError:
#     print('a')


    # trends1 = api.trends_place(1) # from the end of your code
    # # trends1 is a list with only one element in it,which is a
    # # dict which we'll put in data.
    # data = trends1[0]
    # # grab the trends
    # trends = data['trends']
    # # grab the name from each trend
    # names = [trend['name'] for trend in trends]
    # # put all the names together with a ' ' separating them
    # trendsName = '\n'.join(names)
    # print(trendsName)
