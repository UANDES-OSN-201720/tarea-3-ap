#create an INET, STREAMing socket
import socket
import threading
from time import sleep
from socket import error as SocketError
import errno
import re
import sys

closelock=threading.Lock()
close=0
def receiver(msges,acc):
	(recvsock,address)=acc.accept()
	socket=mysocket(recvsock)
	global closelock
	global close
	while(msges>0):
		msg=socket.myreceive()
		if(msg==False or msg=="DISCONNECT"):
			socket.close()
			return
		print ""
		print msg
		msges-=1
	print ""
	while(True):
		closelock.acquire()
		if(close==1):
			socket.close()
			closelock.release()
			return
		closelock.release()
		
		msg=socket.myreceive()
		if(msg==False or msg=="DISCONNECT"):
			print "disconnecting"
			socket.close()
			return
		print msg
	
	
class mysocket:
	def close(self):
		self.sock.close()
	def __init__(self, sock=None):
	    if sock is None:
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    else:
		self.sock = sock
	def connect(self,host, port):
	    self.sock.connect((host, port))
	   
	def mysend(self,msg):
	    msg+='\n'
	    sent = self.sock.send(msg)
		
	    return sent
	def myreceive(self):
	    msg = ''
	    char=''
	    while char!='\n':
	    	msg+=char
		try:
			char =self.sock.recv(1)
		except SocketError as e:
		    if e.errno != errno.ECONNRESET:
			raise # Not error we are looking for
		    return False
		while(char==''):
			
			try:
			    char =self.sock.recv(1)
			except SocketError as e:
			    if e.errno != errno.ECONNRESET:
				raise # Not error we are looking for
			    return False
	
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
sendsock =mysocket()


sendsock.connect("127.0.0.1", 7000)
resp=sendsock.myreceive()
if(resp==False):
	print "DISCONNECTED FROM SERVER\n"
	sys.exit()
print resp
print "CONNECTED"	
command=raw_input("")
sendsock.mysend(command)
acc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
acc.bind(('', 45000))
acc.listen(1)


resp=sendsock.myreceive()
result=re.match("OK \((\d+)\) *",resp)
total=0
if(result is not None):
	total=int(result.groups()[0])
	
else:
	sys.exit()
t=threading.Thread(target=receiver,args=(total,acc))
t.start()
sleep(2)
sendsock.mysend("OK")

print resp

sleep(2)
while(True):
	
	msg=raw_input("Ingrese mensaje para enviar: ")
	if(msg=="DISCONNECT"):
		
		sendsock.mysend("DISCONNECT")
		#############
		break
	sendsock.mysend(msg)
	resp=sendsock.myreceive()
	if(resp==False):
		closelock.acquire()
		close=1
		closelock.release()
		break				
	print resp
	
print "closing princ. thread"
acc.close()
sendsock.sock.close()

