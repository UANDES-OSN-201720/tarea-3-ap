#create an INET, STREAMing socket
import socket
import threading

def listener(socket):
	while(True):
		
class mysocket:
	
	def __init__(self, sock=None):
	    if sock is None:
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    else:
		self.sock = sock
	def connect(self,host, port):
	    self.sock.connect((host, port))
	def mysend(self,msg):
	    sent = self.sock.send(msg)
		
	    return sent
	def register(self,name,password):
		msg="RUSER "+name+" "+password
		sent=self.sock.send(msg)
		if(sent==0):
			print error
	def myreceive(self):
	    msg = ''
	    char=''
	    while char!='\n':
	    	msg+=char
		char =self.sock.recv(1)
		while(char==''):
			char =self.sock.recv(1)
	
	
	    return msg.strip()
	def greet(self,user,password,t):
		msg=""
		if(t=='r'):
			msg+="RUSER"
		else:
			msg+="USER"
		msg+=" "+user+" "+password
		sent=self.mysend(msg)
		if(sent==0):
			return None
		resp=self.myreceive()
		return resp
mysocket =mysocket()


mysocket.connect("127.0.0.1", 27000)
resp=mysocket.myreceive()

print resp
print "CONNECTED"
ing=raw_input("")

mysocket.mysend(ing)
resp=mysocket.myreceive()
print resp
if(resp=="NOT"):	
	pass
	#retorna
acc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
acc.bind(('', 50000))
(torecv,address)=acc.accept()

mysocket.sock.close()
