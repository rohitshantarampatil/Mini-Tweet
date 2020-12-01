from pymongo import MongoClient 
from datetime import datetime
def add_dummy_tweets(db):
	tweets = ["This is tweet1","This is tweet2","This is tweet3"]
	usernames =[]
	timestamps = []
	hashtags = []
	for i in range(3):
		username =db.users.find_one()['username']
		usernames.append(username)
		timestamps.append(datetime.now())
		hashtags.append(['hashtag{0}'.format(i)])
	for i in range(len(usernames)):
		tweet = {
		'tweet':tweets[i],
		'username':usernames[i],
		'hashtags':hashtags[i],
		'timestamp':timestamps[i],
		'retweeted':None,
		'retweeted_from':None,
		}
		db.tweets.insert_one(tweet)
		print('created tweets')
	return True

def add_dummy_users(db):
	usernames = ['rohit','Rohit','Anubhav','Harshil']		
	passwords = ['rohit','Rohit','Anubhav','Harshil']
	lastlogins = [None,None,None,None]
	following = [None,None,None,None]
	followers = [None,None,None,None]

	for i in range(len(usernames)):
		user = {
		'username':usernames[i],
		'password':passwords[i],
		'last_login':lastlogins[i],
		'followers':[],
		'following':[],
		'online':False
		}
		result = db.users.insert_one(user)
		print('created user- {0}'.format(result))

client = MongoClient('localhost',27017)
db = client.minitweet
add_dummy_users(db)
add_dummy_tweets(db)




