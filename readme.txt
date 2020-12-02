# Mini-tweet

A terminal based twitter-like app made from scratch using socket programming.

Following python libraries have to be installed explicitly:

pip install pymongo
pip install stdiomask
pip install termcolor

Mongodb installation required

To use the program:
in Terminal 1: mongod
in Terminal 2: python server.py localhost
in Terminal 3: python client.py localhost


## Installing mongodb:

Ibuntu 20.04

wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -

if success then skip next 2 commands:
	sudo apt-get install gnupg
	wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -


echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

sudo apt-get update
sudo apt-get install -y mongodb-org



## Important instructions: 

You have to create a database named 'minitweet' in MongoDB

To do so:

Run the script db_initiate.py to add some dummy users and tweets in the database.


To run the application on Ubuntu terminal:

python server.py <ip>
python client.py <server_ip>

For example: 

MongoDB should be running (use sudo mongod command)

In terminal 1: run 
python server.py localhost

In terminal 2: run
python client.py localhost

To run application on Mininet

Run mininet using -x flag (for XTerm terminals for each hosts)

Run mongod on the mininet terminal
Run server.py on h1's xterm terminal 
Run client.py on h2's xterm terminal

For example,

mininet -x
mininet> h1 mongod

On h1's xterm terminal, (h1’s IP is by default 10.0.0.1)

python server.py 10.0.0.1 

On h2's xterm terminal,

python client.py 10.0.0.1


To run application on mininet using python script (mininet library for python, taking stdin input for client using .txt files) 

In client.py,
(stdiomask library has been used to hide entered password, this library does not work well with stdin input from .txt files)

Comment lines 52 and 74 
Uncomment lines 53,54,75,76

cd testing
sudo python script_exp.py
