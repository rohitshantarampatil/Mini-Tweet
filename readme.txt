Mini-tweet
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


installing mongodb:

ubuntu 20.04

wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -

if success then skip next 2 commands:
	sudo apt-get install gnupg
	wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -


echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

sudo apt-get update
sudo apt-get install -y mongodb-org


