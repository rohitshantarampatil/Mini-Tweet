import threading
import socket
import argparse
import os
from pymongo import MongoClient 
from login import *
from constants import *


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
	"""
	Supports communications with a connected client.
	Attributes:
	    sc (socket.socket): The connected socket.
	    sockname (tuple): The client socket address.
	    server (Server): The parent thread.
	"""
	def __init__(self, sc, sockname, server):
		super().__init__()
		self.sc = sc
		self.sockname = sockname
		self.server = server
		self.db_client = None
	def connect_to_db(self):
		client = MongoClient('localhost',27017)
		print("database connected")
		return client 


	def run(self):
		self.db_client = self.connect_to_db()

		while True:
			message = self.sc.recv(1024).decode('ascii')
			print("got message")
			# print(message)
			if message:
				#LOGIN
				message = message.split(SEPARATOR)
				if message[0]=='LOGIN':
					try:
						username = message[1]
						password = message[2]
						login_success = login(self.db_client.minitweet,username,password)
						if login_success :
							print('Login successful for user: {0}'.format(username))	
							message = 'LOGIN SUCCESS'
							self.sc.send(message.encode('ascii'))
							break
						else:
							print('Login failed for user: {0}'.format(username))
							message = 'LOGIN FAILED'
							self.sc.sendall(message.encode('ascii'))
					except:
						message = 'LOGIN FAILED'
						self.sc.sendall(message.encode('ascii'))

				elif message[0]=='REGISTER':
					try:
						username = message[1]
						password = message[2]
						print('verifying registration')
						register_success = register(self.db_client.minitweet,username,password)
						print(register_success)
						if register_success :
							print('Registration successful for user: {0}'.format(username))
							message = 'REGISTRATION SUCCESS'
							self.sc.send(message.encode('ascii'))
						else:
							print('Registration failed for user: {0}'.format(username))
							message = 'REGISTRATION FAILED'
							self.sc.sendall(message.encode('ascii'))
					except:
						message = 'REGISTRATION FAILED'
						self.sc.sendall(message.encode('ascii'))		

			else:
				# Client has closed the socket, exit the thread
				print('{} has closed the connection'.format(self.sockname))
				self.sc.close()
				server.remove_connection(self)
				return
			

		# while True:
		#     message = self.sc.recv(1024).decode('ascii')
		#     if message:
		#         pass

		#     else:
		#         # Client has closed the socket, exit the thread
		#         print('{} has closed the connection'.format(self.sockname))
		#         self.sc.close()
		#         server.remove_connection(self)
		#         return


def exit(server):
	"""
	Allows the server administrator to shut down the server.
	Typing 'q' in the command line will close all active connections and exit the application.
	"""
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

