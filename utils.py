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

def del_tweet_by_id(db,tweet_id):
	try:
		db.tweets.delete_one({'_id':tweet_id})
		return True
	except:
		return False


################################################################################

################################# Show userfeed ###############################

def feed_display(db,username):
	user = list(db.users.find({'username':username}))
	dict1 = user[0]
	user_following = dict1['following']
	#print(user_following)
	tweets = []
	if not user_following:
		return []

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




##################################################################################

############################### Show All Users #################################

def show_users(db,username):
	user_list = []
	all_users = db["users"].find()
	for i in all_users:
		if i["username"]!=username:
			if(not i["followers"]):
				user_list.append({"username":i["username"],"Follow":"You do not follow him"})
			elif(username in i["followers"]):
				user_list.append({"username":i["username"],"Follow":"You follow him"})
			else:
				user_list.append({"username":i["username"],"Follow":"You do not follow him"})
	return user_list

def follow_user(db,username,username_to_follow):
	user1 = db.users.find_one({'username':username})
	following = user1["following"]

	if(not following):
		new_following = [username_to_follow]
	elif(username_to_follow in following):
		return False;
	else:
		new_following = following + [username_to_follow]

	db.users.update_one({'username':username},{"$set": {"following":new_following}})

	user2 = db.users.find_one({'username':username_to_follow})
	followers = user2["followers"]

	if(not followers):
		new_followers = [username]
	else:
		new_followers = followers + [username]

	db.users.update_one({'username':username_to_follow},{"$set": {"followers":new_followers}})
	return True

def unfollow_user(db,username,username_to_unfollow):
	user1 = db.users.find_one({'username':username})
	following = user1["following"]

	if(not following):
		return False;
	elif(username_to_unfollow not in following):
		return False;
	else:
		following.remove(username_to_unfollow)

	new_following = following[:]
	db.users.update_one({'username':username},{"$set": {"following":new_following}})

	user2 = db.users.find_one({'username':username_to_unfollow})
	followers = user2["followers"]

	if(not followers):
		return False;
	else:
		followers.remove(username)

	new_followers = followers[:]
	db.users.update_one({'username':username_to_unfollow},{"$set": {"followers":new_followers}})
	return True

################################################################################

############################### Show All Followings and Followers #############################

def show_following(db,username):
	following_list = db.users.find_one({"username": username})["following"]
	online_list = []

	for i in following_list:
		online_stat = db.users.find_one({"username": i})["online"]
		if(online_stat):
			online_list.append("Online")
		else:
			online_list.append("Not Online")

	if(not following_list):
		return [],[]
	return following_list,online_list

def show_followers(db,username):
	followers_list = db.users.find_one({"username": username})["followers"]
	online_list = []

	for i in followers_list:
		online_stat = db.users.find_one({"username": i})["online"]
		if(online_stat):
			online_list.append("Online")
		else:
			online_list.append("Not Online")

	if(not followers_list):
		return [],[]
	return followers_list,online_list

################################################################################

################################## Search Tweets ###############################
def search_tweets(db,search_text,my_username):
	db.tweets.create_index([("tweet","text"),("username","text")])
	tweets =db.tweets.find({"$text":{"$search":search_text}}).limit(10)
	if not tweets:
		return []
	lst = []
	for i in tweets: 
		if i["username"]!=my_username:
			lst.append({"tweet":i['tweet'],'_id':i['_id'],'timestamp':i['timestamp'],'username':i['username']})
	return lst

def search_my_tweets(db,search_text,my_username):
	db.tweets.create_index([("tweet","text"),("username","text")])
	tweets =db.tweets.find({"$text":{"$search":search_text}}).limit(10)
	if not tweets:
		return []
	lst = []
	for i in tweets: 
		if i["username"]==my_username:
			lst.append({"tweet":i['tweet'],'_id':i['_id'],'timestamp':i['timestamp'],'username':i['username']})
	return lst

#show trending hashtags
def get_trending_hashtags(db):
	tweets = db.tweets.find({})
	hashtags = {}
	for i in tweets:
		if i['hashtags']!=None:
			for k in i['hashtags']:
				if k in hashtags:
					hashtags[k]+=1
				else:
					hashtags[k]=1
	lst= [[i,hashtags[i]] for i in hashtags]
	lst.sort(key = lambda x:x[1],reverse=True)
	if lst:
		return lst[:5]
	return []

#################################################################################


# from pymongo import MongoClient
# client = MongoClient('localhost',27017)
# db = client.minitweet
# tweets = get_tweets(db,'rohit')
# tweets = dumps(tweets)
# # print(tweets)
# tweets = loads(tweets)
# print(tweets[0]['timestamp'])
# text = "#modi"

# lst = search_tweets(db,text)
# lst = get_trending_hashtags(db)
# print(lst)