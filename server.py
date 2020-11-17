import threading
import socket
import argparse
import os
from pymongo import MongoClient 
from login import *
from constants import *
from utils import *
import json
from bson.json_util import dumps,loads


class Server(threading.Thread):
	def __init__(self, host, port):
		super().__init__()
		self.connections = []
		self.host = host
		self.port = port

	def run(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind((self.host, self.port))

		sock.listen(1)
		print('Listening at', sock.getsockname())

		while True:

			# Accept new connection
			sc, sockname = sock.accept()
			print('Accepted a new connection from {} to {}'.format(sc.getpeername(), sc.getsockname()))

			# Create new thread
			server_socket = ServerSocket(sc, sockname, self)

			# Start new thread
			server_socket.start()

			# Add thread to active connections
			self.connections.append(server_socket)

	def remove_connection(self, connection):
		self.connections.remove(connection)

class ServerSocket(threading.Thread):
	'''
	Supports communications with a connected client.
	Attributes:
	    sc (socket.socket): The connected socket.
	    sockname (tuple): The client socket address.
	    server (Server): The parent thread.
	'''
	def __init__(self, sc, sockname, server):
		super().__init__()
		self.sc = sc
		self.sockname = sockname
		self.server = server
		self.db_client = None
		self.username = None
	def connect_to_db(self):
		client = MongoClient('localhost',27017)
		print('database connected')
		return client 


	def run(self):
		self.db_client = self.connect_to_db()

		while True:
			message = self.sc.recv(1024).decode('ascii')
			# print(message)
			if message:
				print('got message from login screen')
				print()
				#LOGIN
				message = message.split(SEPARATOR)
				if message[0]=='LOGIN':
					try:
						username = message[1]
						password = message[2]
						login_success = login(self.db_client.minitweet,username,password)
						if login_success :
							self.username = username
							print('Login successful for user: {0}'.format(username))	
							response = 'LOGIN SUCCESS'
							self.sc.send(response.encode('ascii'))
							break
						else:
							print('Login failed for user: {0}'.format(username))
							response = 'LOGIN FAILED'
							self.sc.sendall(response.encode('ascii'))
					except:
						response = 'LOGIN FAILED'
						self.sc.sendall(response.encode('ascii'))

				elif message[0]=='REGISTER':
					try:
						username = message[1]
						password = message[2]
						print('verifying registration')
						register_success = register(self.db_client.minitweet,username,password)
						print(register_success)
						if register_success :
							print('Registration successful for user: {0}'.format(username))
							response = 'REGISTRATION SUCCESS'
							self.sc.send(response.encode('ascii'))
						else:
							print('Registration failed for user: {0}'.format(username))
							response = 'REGISTRATION FAILED'
							self.sc.sendall(response.encode('ascii'))
					except:
						response = 'REGISTRATION FAILED'
						self.sc.sendall(response.encode('ascii'))

			else:
				# Client has closed the socket, exit the thread
				print('{} has closed the connection'.format(self.sockname))
				self.sc.close()
				server.remove_connection(self)
				return


		while True:
			message = self.sc.recv(1024).decode('ascii')
			if message:
				print('got message from screen 2 for user: {0}'.format(self.username))
				message = message.split(SEPARATOR)
				
				if message[0]=='POST TWEET':
					tweet = message[1]
					post = post_tweet(self.db_client.minitweet,tweet,self.username)
					if post==True:
						print('Tweet posted for user : {}'.format(self.username))
						response ='TWEET POST SUCCESS'
						self.sc.sendall(response.encode('ascii'))
					else:
						print('Tweet failed for user : {}'.format(self.username))
						response ='TWEET POST FAILED'
						self.sc.sendall(response.encode('ascii'))
				
				elif message[0]=='PROFILE':
					tweet_list = get_tweets(self.db_client.minitweet,self.username)
					response = dumps(tweet_list)
					self.sc.sendall(response.encode('ascii'))
					#Now waiting for next choice(delete or back)
					response_mini = self.sc.recv(1024).decode('ascii')
					response_mini = loads(response_mini)
					if response_mini['type']=='BACK':
						continue
					else:
						tweet_id_to_delete = response_mini['_id']
						deleted = del_tweet_by_id(self.db_client.minitweet, tweet_id_to_delete)
						if deleted:
							response_mini = 'DEL TWEET SUCCESS'
							self.sc.sendall(response_mini.encode('ascii'))
						else:
							response_mini = 'DEL TWEET FAILED'
							self.sc.sendall(response_mini.encode('ascii'))

				elif message[0]=='SHOW FOLLOWERS':
					followers_list = show_followers(self.db_client.minitweet, self.username)
					response = dumps(followers_list)
					self.sc.sendall(response.encode('ascii'))

					# Now waiting for next choice (whether to remove a given follower)
					response_mini = self.sc.recv(1024).decode('ascii')
					response_mini = loads(response_mini)

					if response_mini['type']=='BACK':
						continue

					else:
						username_to_remove = response_mini['username']
						user_remove = unfollow_user(self.db_client.minitweet, username_to_remove, self.username)
						if user_remove:
							response_mini = 'REMOVE FOLLOWER SUCCESS'
							self.sc.sendall(response_mini.encode('ascii'))
						else:
							response_mini = 'REMOVE FOLLOWER FAILED'
							self.sc.sendall(response_mini.encode('ascii'))
				
				elif message[0]=='SHOW FOLLOWING':
					following_list = show_following(self.db_client.minitweet, self.username)
					response = dumps(following_list)
					self.sc.sendall(response.encode('ascii'))

					# Now waiting for next choice (whether to unfollow a given user)
					response_mini = self.sc.recv(1024).decode('ascii')
					response_mini = loads(response_mini)

					if response_mini['type']=='BACK':
						continue

					else:
						username_to_unfollow = response_mini['username']
						user_unfol = unfollow_user(self.db_client.minitweet, self.username, username_to_unfollow)
						if user_unfol:
							response_mini = 'UNFOLLOW USER SUCCESS'
							self.sc.sendall(response_mini.encode('ascii'))
						else:
							response_mini = 'UNFOLLOW USER FAILED'
							self.sc.sendall(response_mini.encode('ascii'))
				
				elif message[0]=='SHOW USERS':
					user_list = show_users(self.db_client.minitweet, self.username)
					response = dumps(user_list)
					self.sc.sendall(response.encode('ascii'))

					# Now waiting for next choice (whether to follow/unfollow a given user)
					response_mini = self.sc.recv(1024).decode('ascii')
					response_mini = loads(response_mini)

					if response_mini['type']=='BACK':
						continue

					elif response_mini['type']=='FOL USER':
						username_to_follow = response_mini['username']
						user_fol = follow_user(self.db_client.minitweet, self.username, username_to_follow)
						if user_fol:
							response_mini = 'FOLLOW USER SUCCESS'
							self.sc.sendall(response_mini.encode('ascii'))
						else:
							response_mini = 'FOLLOW USER FAILED'
							self.sc.sendall(response_mini.encode('ascii'))

					else:
						username_to_unfollow = response_mini['username']
						user_unfol = unfollow_user(self.db_client.minitweet, self.username, username_to_unfollow)
						if user_unfol:
							response_mini = 'UNFOLLOW USER SUCCESS'
							self.sc.sendall(response_mini.encode('ascii'))
						else:
							response_mini = 'UNFOLLOW USER FAILED'
							self.sc.sendall(response_mini.encode('ascii'))
				else:
					print('something else')

			else:
				# Client has closed the socket, exit the thread
				print('{} has closed the connection'.format(self.sockname))
				self.sc.close()
				server.remove_connection(self)
				return


def exit(server):
	'''
	Allows the server administrator to shut down the server.
	Typing 'q' in the command line will close all active connections and exit the application.
	'''
	while True:
		ipt = input('')
		if ipt == 'q':
			print('Closing all connections...')
			for connection in server.connections:
			    connection.sc.close()
			print('Shutting down the server...')
			os._exit(0)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Mini Tweet')
	parser.add_argument('host', help='Interface the server listens at')
	parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port (default 1060)')
	args = parser.parse_args()

	# Create and start server thread
	server = Server(args.host, args.p)
	server.start()
	exit = threading.Thread(target = exit, args = (server,))

