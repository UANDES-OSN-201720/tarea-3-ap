
import threading
import socket
import re
users={}
logins={}

def login(user,pwd):
	global logins
	if user in logins:
		if(logins[user]==pwd):
			return True
		else:
			return False
	else:
		return False
def register(user,pwd):
	global logins
	if user in logins:
		return False
	logins[user]=pwd
	
	return True
def thread(socket):
	global users
	global logins
	print "hola"
	socket.mysend("OK\n")
	login=socket.myreceive()
	result=re.match("(USER) ([a-z]*) ([a-z]*)",login)
	if result is not None:
		(opt,user,pw)=result.groups()
		nicks=logins.keys()
		if(opt=="USER"):
			if(login(user,pwd)):
			socket.mysend("OK\n")
			
	else:
		socket.mysend("BAD COMMAND\n")
		socket.sock.close()
		return
	tosend=mysocket()
	tosend.connect("127.0.0.1", 5000)
	
class mysocket:
	global users
	def __init__(self, sock=None):
	    if sock is None:
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    else:
		self.sock = sock
	def connect(host, port):
	    self.sock.connect((host, port))
	def mysend(self,msg):
	    sent = self.sock.send(msg)
	    return sent
	def myreceive(self):
	    msg = ''
	    char=''
	    while char!='\n':
	    	msg+=char
		char =self.sock.recv(1)
		while(char==''):
			char =self.sock.recv(1)
	
	
	    return msg.strip()
	def greet(self):
		msg=self.myreceive()
		
f=open("record.txt",'r')
f=f.readlines()
for i in f:
	temp=i.strip()
	(user,password)=temp.split(' ')
	logins[user]=password
print logins
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind(('', 27000))
#become a server socket
serversocket.listen(5)
(csocket, address) = serversocket.accept()
clientsocket=mysocket(csocket)
t=threading.Thread(target=thread,args=(clientsocket,))
t.start()


serversocket.close()


