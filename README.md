# Mini-Tweet

A terminal based Twitter-like app made from scratch using socket programming.

Following python libraries have to be installed explicitly:

```bash
pip install pymongo

pip install stdiomask

pip install termcolor
```

MongoDB installation is required

To use the program:

```bash
#in Terminal 1: 

mongod

#in Terminal 2: 

python server.py localhost

#in Terminal 3: 

python client.py localhost

```

## Installing MongoDB:

Ubuntu 20.04

```bash
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
```

if success then skip next 2 commands:
```bash
sudo apt-get install gnupg
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
```

```bash
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

sudo apt-get update
sudo apt-get install -y mongodb-org
```


## Important Instructions: 

You have to create a database named 'minitweet' in MongoDB

To do so:

Run the script db_initiate.py to add some dummy users and tweets in the database.


To run the application on Ubuntu terminal:

```bash

python server.py <ip>
python client.py <server_ip>
```

For example: 

MongoDB should be running (use sudo mongod command)

```bash
#In terminal 1: run 

python server.py localhost
```
```bash
#In terminal 2: run

python client.py localhost
```

To run application on Mininet

Run mininet using -x flag (for XTerm terminals for each hosts)

Run mongod on the mininet terminal
Run server.py on h1's xterm terminal 
Run client.py on h2's xterm terminal

For example,

```bash
mininet -x
mininet> h1 mongod

```

On h1's xterm terminal, (h1’s IP is by default 10.0.0.1)

```bash
python server.py 10.0.0.1 
```

On h2's xterm terminal,

```bash
python client.py 10.0.0.1
```

To run application on mininet using python script (Mininet library for python, taking stdin input for client using .txt files) 

In client.py,
(stdiomask library has been used to hide entered password, this library does not work well with stdin input from .txt files)

Comment lines 52 and 74 
Uncomment lines 53,54,75,76

```bash
cd testing
sudo python script_exp.py
```

## Team Members

Harshil Jain
Rohit Patil
Anubhav Jain
