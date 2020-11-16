from pymongo import MongoClient
from datetime import datetime
 
def login(db,username,password):
	try:
		user_exist = db.users.find_one({'username':username})
		if not user_exist:
			#username or password wrong
			return False
		else:
			password_db = user_exist['password']
			_id= user_exist['_id']
			if password_db==password:
				db.users.find_one_and_update({'_id':_id},{'$set':{'last_login': datetime.now(),'online':True}},upsert=True)
				return True
			else:
				return False
	except Exception as e:
		return e

def register(db,username,password):
	user_exist = db.users.find_one({'username':username})
	if user_exist:
		return False
	else:
		user = {
		'username':username,
		'password':password,
		'last_login':None,
		'following':None,
		'followers':None,
		'online':None
		}
		try:
			db.users.insert_one(user)
			return True
		except Exception as e:
			return e

# def logout(db,username):
# 	try:
# 		user_exist = db.users.find_one({'username':username})	
# 		db.users.find_one_and_update({'_id':_id},{'$set':{'online':False}},upsert=True)
# 		return True	

# 	except Exception as e:
# 		return e

def delete_user(db,username,password):
	try:
		user_exist = db.users.find_one({'username':username})
		if not user_exist:
			#username or password wrong
			return False
		else:
			password_db = user_exist['password']
			if password_db==password:
				db.users.delete_one({'username':username})
				return True
			else:
				return False
	except Exception as e:
		return e



# client = MongoClient('localhost',27017)
# db = client.minitweet
# username = "Rohita"
# password = 'Rohit'
# print(register(db,username,password))
# print(login(db,username,password))
# print(delete_user(db,username,password))
# print(login(db,username,password))

