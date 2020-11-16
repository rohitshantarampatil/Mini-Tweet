import threading
import socket
import argparse
import os
import sys
import stdiomask
from constants import *
from utils import *
from bson.json_util import dumps,loads

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
			# print('8. Logout')
			#other options
			print('write exit to close the program \n')
			print()	
			
			inp = input()	
			print()

			if inp=='exit':
				self.sock.close()
				os._exit(0)

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
			
			#REST OF The functions

			# if inp=="8":
			# 	message = 'LOGOUT'
			# 	self.sock.sendall(message.encode('ascii'))
			# 	self.sock.close()
			# 	os._exit(0)




def main(host,port):
	client = Client(host,port)
	client.start()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Mini Tweet')
	parser.add_argument('host', help='Interface the server listens at')
	parser.add_argument('-p', metavar='PORT', type=int, default=1060,help='TCP port (default 1060)')
	args = parser.parse_args()
	main(args.host, args.p)
