import sys
import time
from datetime import datetime
from termcolor import colored
import re



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