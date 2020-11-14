from pymongo import MongoClient 

try:
	client = MongoClient('localhost',27017)
	db = client.minitweet
	usernames = ['Rohit']
	passwords = ['Rohit']
	lastlogins = [None]

	for i in range(len(usernames)):
		user = {
		'username':usernames[i],
		'password':passwords[i],
		'last_login':lastlogins[i]
		}
		result = db.users.insert_one(user)
		print('created user- {0}'.format(result))


except Exception as e:
	print(e)