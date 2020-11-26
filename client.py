import threading
import socket
import argparse
import os
import sys
import stdiomask
from constants import *
from utils import *
from bson.json_util import dumps,loads
import time

class Client:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def start(self):
		'''
		Establishes the client-server connection. Gathers user input for the username,
		creates and starts the Send and Receive threads, and notifies other connected clients.
		Returns:
		A Receive object representing the receiving thread.
		'''
		print('Trying to connect to {}:{}...'.format(self.host, self.port))
		self.sock.connect((self.host, self.port))
		print('Successfully connected to {}:{}'.format(self.host, self.port))
		print()
		print('Welcome to MiniTweet')
		while True:
			print('select from following options')
			print()
			print('1. Register ')
			print('2. Login \n\n')
			print('write exit to close the program \n')
			
			inp = input()	
			if inp=='exit':
				self.sock.close()
				os._exit(0)
			

			#Checking if inputs are non-empty
			if not check_input_string([inp]):
				print('Bad input,Try again')
				continue
			

			if inp=='1':
				print('Username: ',end='')
				username= input()
				password = stdiomask.getpass()
				
				#Checking if inputs are non-empty
				if not check_input_string([username,password]):
					print('Bad input,Try again')
					continue

				message = 'REGISTER{0}{1}{2}{3}'.format(SEPARATOR,username,SEPARATOR,password)

				self.sock.sendall(message.encode('ascii'))
				print()
				response = self.sock.recv(1024).decode('ascii')
				if response=='REGISTRATION SUCCESS':
					print('Registration successfully completed, now please login using your credentials\n')
					continue
				elif response=='REGISTRATION FAILED':
					print('Registration Failed, username already exists, please try different username\n')
					continue
			elif inp=='2':
				print('Username: ',end='')
				username= input()
				password = stdiomask.getpass()
				message = 'LOGIN{0}{1}{2}{3}'.format(SEPARATOR,username,SEPARATOR,password)
				self.sock.sendall(message.encode('ascii'))
				response = self.sock.recv(1024).decode('ascii')
				print()
				if response=='LOGIN SUCCESS':
					print('Login success\n')
					break
				elif response=='LOGIN FAILED':
					print('Login failed, username or password is incorrect\n')
					continue      		
		
		###Further code in following while true loop
		while  True:
			print('select from following options')
			print()
			print('1. Post Tweet ')
			print('2. Profile [Show/Delete my tweets] ')
			print('3. Show User Feed [Retweet a tweet]')
			print('4. Search Tweets / Show trending tweets')
			print('6. Show Followers[Show/Remove a follower]')
			print('7. Show Followings[Show/Unfollow]')
			print('8. Show all Users [Show/Follow or Unfollow]')
			print('9. Logout')
			#other options
			
			inp = input()	
			print()


			if not check_input_string([inp]):
				print('Bad input,Try again')
				continue

			if inp=='1':
				print('Post Tweet selected')
				print()
				print('Type text:',end='')
				
				tweet = input()

				if not check_input_string([tweet]):
					print('Bad input,Try again')
					print()
					continue

				message = 'POST TWEET{0}{1}'.format(SEPARATOR,tweet)
				self.sock.sendall(message.encode('ascii'))
				response = self.sock.recv(1024).decode('ascii')
				if response == 'TWEET POST SUCCESS':
					print('Tweet posted successfully')
					print()
					continue
				else:
					print('Tweet posting failed')
					print()
					continue
			if inp=='2':
				print('Profile selected')

				message = 'PROFILE'
				self.sock.sendall(message.encode('ascii'))
				print('Showing all tweets,please wait ...')
				response = self.sock.recv(1024).decode('ascii')
				response = loads(response)
				print()

				if len(response)==0:
					print()
					print("You haven't posted any tweet yet")
					print()
					message_mini = {'type':'BACK'}
					message_mini = dumps(message_mini)
					self.sock.sendall(message_mini.encode('ascii'))					
					continue
				else:
					for i in range(len(response)):
						print("{0}:{1} \n{2} \n".format(i+1,response[i]['tweet'], response[i]['timestamp'].date()))
						
					print('1. Delete tweet')
					print("2. Back")
					choice = input()
					if choice=="1":
						print("Enter Tweet Number")
						num = int(input())-1
						message_mini ={'type':"DEL TWEET",'_id':response[num]['_id']}
						message_mini = dumps(message_mini)
						self.sock.sendall(message_mini.encode('ascii'))
						response_mini = self.sock.recv(1024).decode('ascii')
						if response_mini=="DEL TWEET SUCCESS":
							print()
							print("Tweet deleted successfully")
							print()
						else:
							print()
							print("Tweet deletion failed")
							print()
					elif choice=='2':
						message_mini = {'type':'BACK'}
						message_mini = dumps(message_mini)
						self.sock.sendall(message_mini.encode('ascii'))
						print()
			
			if inp=='3':
				print("User Feed will be displayed")
				message = "ALLUSERFEED"
				self.sock.sendall(message.encode('ascii'))
				print("Showing all user feed, please wait ...")
				response = self.sock.recv(1024).decode('ascii')
				response = loads(response)
				# print("response{0}",response)
				print()
				if len(response)==0:
					print("There are no tweets posted from users you follow.")
					message_mini ={'type':"BACK"}
					message_mini = dumps(message_mini)
					self.sock.sendall(message_mini.encode('ascii'))
					continue

				else:
					for i in range(len(response)):
						print(response[i]['username'],end = " ")
						print("tweeted this tweet")
						print("{0}:{1} \n{2} \n".format(i+1,response[i]['tweet'], response[i]['timestamp'].date()))
					print("1. Retweet a tweet")
					print("2. Back")
					choice = input()
					if choice == '1':
						print("Enter Tweet Number")
						num = int(input())-1
						message_mini ={'type':"RETWEET",'tweet':response[num]['tweet'],'username':response[num]['username']}
						message_mini = dumps(message_mini)
						self.sock.sendall(message_mini.encode('ascii'))
						response_mini = self.sock.recv(1024).decode('ascii')
						if response_mini=="RETWEET SUCCESS":
							print()
							print("Tweet retweeted successfully")
							print()
					else:
						message_mini ={'type':"BACK"}
						message_mini = dumps(message_mini)
						self.sock.sendall(message_mini.encode('ascii'))
						continue
			if inp=='4':
				print("1. search tweets")
				print("2. show top 5 trending hashtags")
				choice = input()
				if choice=="1":
					print()
					print("Type search text : you can enter usernames or hashtags or tweet text anything...")
					search_text = input()
					if not check_input_string([search_text]):
						continue
					message = "SEARCH FEED{0}{1}".format(SEPARATOR,search_text)
					self.sock.sendall(message.encode('ascii'))
					response = self.sock.recv(1024).decode('ascii')
					response = loads(response)
					print()

					if len(response)==0:
						print("There are no tweets which match your search")
						message_mini ={'type':"BACK"}
						message_mini = dumps(message_mini)
						self.sock.sendall(message_mini.encode('ascii'))
						continue

					else:
						for i in range(len(response)):
							print(response[i]['username'],end = " ")
							print("tweeted this tweet")
							print("{0}:{1} \n{2} \n".format(i+1,response[i]['tweet'], response[i]['timestamp'].date()))
						print("1. Retweet a tweet")
						print("2. Back")
						choice = input()
						if choice == '1':
							print("Enter Tweet Number")
							num = int(input())-1
							message_mini ={'type':"RETWEET",'tweet':response[num]['tweet'],'username':response[num]['username']}
							message_mini = dumps(message_mini)
							self.sock.sendall(message_mini.encode('ascii'))
							response_mini = self.sock.recv(1024).decode('ascii')
							if response_mini=="RETWEET SUCCESS":
								print()
								print("Tweet retweeted successfully")
								print()
						else:
							message_mini ={'type':"BACK"}
							message_mini = dumps(message_mini)
							self.sock.sendall(message_mini.encode('ascii'))
							continue
				
				elif choice=="2":
					message = "TRENDING HASHTAGS"
					self.sock.sendall(message.encode('ascii'))
					response = self.sock.recv(1024).decode('ascii')
					response = loads(response)
					
					if response:
						print("here are top 5 trending hashtags")
						for i in response:
							print(i)
					else:
						print("no tweets available")
						print()

			if inp=='6':
				print('Show all followers selected')

				message = 'SHOW FOLLOWERS'
				self.sock.sendall(message.encode('ascii'))
				print('Showing all followers,please wait ...')
				response = self.sock.recv(1024).decode('ascii')
				response = loads(response)

				online_list = response[1]
				response = response[0]
				print()

				if len(response)==0:
					print()
					print("You don't have any followers yet")
					print()
					message_mini = {'type':'BACK'}
					message_mini = dumps(message_mini)
					self.sock.sendall(message_mini.encode('ascii'))					
					continue

				else:
					for i in range(len(response)):
						print("{0}:{1}\t{2} \n".format(i+1,response[i],online_list[i]))
						
					print('1. Remove a given follower')
					print("2. Back")
					choice = input()
					print()
					if (choice =="1"):
						print("Enter the user number which you want to remove")
						u_num = int(input())-1

						message_mini ={'type':"UNFOL USER",'username':response[u_num]}
						message_mini = dumps(message_mini)
						self.sock.sendall(message_mini.encode('ascii'))
						response_mini = self.sock.recv(1024).decode('ascii')

						if response_mini=="REMOVE FOLLOWER SUCCESS":
							print()
							print("You have successfully removed the follower")
							print()
						else:
							print()
							print("Error!!!")
							print()

					elif (choice=='2'):
						message_mini = {'type':'BACK'}
						message_mini = dumps(message_mini)
						self.sock.sendall(message_mini.encode('ascii'))
						print()
			if inp=='7':
				print('Show all following selected')

				message = 'SHOW FOLLOWING'
				self.sock.sendall(message.encode('ascii'))
				print('Showing all followings,please wait ...')
				response = self.sock.recv(1024).decode('ascii')
				response = loads(response)

				online_list = response[1]
				response = response[0]
				print()

				if len(response)==0:
					print()
					print("You don't have any followings yet")
					print()
					message_mini = {'type':'BACK'}
					message_mini = dumps(message_mini)
					self.sock.sendall(message_mini.encode('ascii'))					
					continue

				else:
					for i in range(len(response)):
						print("{0}:{1}\t{2} \n".format(i+1,response[i],online_list[i]))
						
					print('1. Unfollow a given user')
					print("2. Back")
					choice = input()
					print()
					if (choice =="1"):
						print("Enter the user number which you want to unfollow")
						u_num = int(input())-1

						message_mini ={'type':"UNFOL USER",'username':response[u_num]}
						message_mini = dumps(message_mini)
						self.sock.sendall(message_mini.encode('ascii'))
						response_mini = self.sock.recv(1024).decode('ascii')

						if response_mini=="UNFOLLOW USER SUCCESS":
							print()
							print("You have successfully unfollowed the user")
							print()
						else:
							print()
							print("Error!!!")
							print()

					elif (choice=='2'):
						message_mini = {'type':'BACK'}
						message_mini = dumps(message_mini)
						self.sock.sendall(message_mini.encode('ascii'))
						print()

			if inp=='8':
				print('Show all users selected')

				message = 'SHOW USERS'
				self.sock.sendall(message.encode('ascii'))
				print('Showing all users,please wait ...')
				response = self.sock.recv(1024).decode('ascii')
				response = loads(response)
				print()

				for i in range(len(response)):
					print("{0}:{1} \n{2} \n".format(i+1,response[i]['username'], response[i]['Follow']))
					
				print('1. Follow a given user')
				print('2. Unfollow a given user')
				print("3. Back")
				choice = input()
				print()
				if (choice =="1"):
					print("Enter the user number which you want to follow")
					u_num = int(input())-1

					message_mini ={'type':"FOL USER",'username':response[u_num]['username']}
					message_mini = dumps(message_mini)
					self.sock.sendall(message_mini.encode('ascii'))
					response_mini = self.sock.recv(1024).decode('ascii')

					if response_mini=="FOLLOW USER SUCCESS":
						print()
						print("You have successfully started following the user")
						print()
					else:
						print()
						print("Error: You already follow that user")
						print()
				elif(choice == "2"):
					print("Enter the user number which you want to unfollow")
					u_num = int(input())-1

					message_mini ={'type':"UNFOL USER",'username':response[u_num]['username']}
					message_mini = dumps(message_mini)
					self.sock.sendall(message_mini.encode('ascii'))
					response_mini = self.sock.recv(1024).decode('ascii')

					if response_mini=="UNFOLLOW USER SUCCESS":
						print()
						print("You have successfully unfollowed the user")
						print()
					else:
						print()
						print("Error: You already don't follow that user")
						print()

				elif(choice=='3'):
					message_mini = {'type':'BACK'}
					message_mini = dumps(message_mini)
					self.sock.sendall(message_mini.encode('ascii'))
					print()
			
			#REST OF The functions

			if inp=="9":
				message = 'LOGOUT'
				self.sock.sendall(message.encode('ascii'))
				response = self.sock.recv(1024).decode('ascii')
				print('logging out...')
				time.sleep(2)
				self.sock.close()
				os._exit(0)




def main(host,port):
	client = Client(host,port)
	client.start()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Mini Tweet')
	parser.add_argument('host', help='Interface the server listens at',default='localhost')
	parser.add_argument('-p', metavar='PORT', type=int, default=1060,help='TCP port (default 1060)')
	args = parser.parse_args()
	main(args.host, args.p)
