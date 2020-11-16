import sys
import time
from datetime import datetime
from termcolor import colored
import re
import json
from bson.json_util import dumps,loads

def delete_last_lines(n):
    "Use this function to delete the last line in the STDOUT"

    for i in range(n):
    	#cursor up one line	
	    sys.stdout.write('\x1b[1A')

	    #delete last line
	    sys.stdout.write('\x1b[2K')


def check_input_string(lst):
	for i in lst:
		if not len(i)>0:
			return False
	return True


################################ Post Tweet Functions #########################
def extract_hashtags(tweet):
	regex = "#\w+"
	lst = re.findall(regex,tweet)
	if lst:
		return lst 
	return []

def post_tweet(db,tweet,username):
	hashtags = extract_hashtags(tweet)
	tweet = {
		'tweet':tweet,
		'username':username,
		'hashtags':hashtags,
		'timestamp':datetime.now(),
		'retweeted':None,
		'retweeted_from':None,
		}
	db.tweets.insert_one(tweet)
	return True


###############################################################################

################################## Profile Functions #########################

def get_tweets(db,username):
	tweets = list(db.tweets.find({'username':username}))
	tweets.sort(key = lambda x:x['timestamp'],reverse =True)
	lst = [{"tweet":i['tweet'],'_id':i['_id'],'timestamp':i['timestamp']} for i in tweets]
	return lst

def feed_display(db,username):
	user = list(db.users.find({'username':username}))
	dict1 = user[0]
	user_following = dict1['following']
	#print(user_following)
	tweets = []
	for i in user_following:
		tweets.extend(list(db.tweets.find({'username':i})))
	tweets.sort(key = lambda x:x['timestamp'],reverse =True)
	lst = [{"tweet":i['tweet'],'_id':i['_id'],'timestamp':i['timestamp'],'username':i['username']} for i in tweets]
	#print(lst)
	return lst

def retweet_func(db,tweet,username_retweet,username):
	hashtags = extract_hashtags(tweet)
	tweet = {
		'tweet':tweet,
		'username':username,
		'hashtags':hashtags,
		'timestamp':datetime.now(),
		'retweeted':True,
		'retweeted_from':username_retweet,
		}
	db.tweets.insert_one(tweet)
	return True

# from pymongo import MongoClient
# client = MongoClient('localhost',27017)
# db = client.minitweet
# tweets = get_tweets(db,'rohit')
# tweets = dumps(tweets)
# # print(tweets)
# tweets = loads(tweets)
# print(tweets[0]['timestamp'])