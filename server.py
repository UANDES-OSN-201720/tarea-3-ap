import sys
import threading
import socket
from socket import error as SocketError
import errno
import re
import random
users=[]
groups=[]
logins={}
threads=[]
closelock=threading.Lock()
close=0

	
def send_groupal_msg(msg,group):
	
	global groups
	pass
	
	for i in groups:
		if(i.name==group):
			i.send_msg(msg)
	
			return True
	
	pass
	return False
	
def addgroup(group):
	global groups
	pass
	groups.append(group)
	pass
def console(var):
	command=raw_input("")
	if(command==""):
		var=1
def get_usrnames():
	global users
	usrnames=[]
	for i in users:
		usrnames.append(i.name)
	return usrnames

class user:
	def __init__(self,name,password,queue=None,sendsock=None):
		self.name=name
		self.password=password
		if(queue is not None):
			self.queue=queue
		else:
			self.queue=[]
		if(sendsock is not None):
			self.sendsock=sendsock
		else:
			self.sendsock=None
	def disconnect(self):	
		self.sendsock.close()
		self.sendsock=None
	def send_msg(self,msg):
		if(self.sendsock is None):
			self.enqueue_msg(msg)
		else:
			sent=self.sendsock.mysend(msg)
			if(sent==0):
				self.enqueue_msg(msg)
	def enqueue_msg(self,msg):
		self.queue.append(msg)
	def desenqueue_msg(self):
		msg=self.queue.pop()
		return msg
	def set_sendsock(self,sendsock):
		self.sendsock=sendsock
		msges=len(self.queue)
		while(msges>0):
			msg=self.desenqueue_msg()
			self.sendsock.mysend(msg)
			msges-=1
def creategroup(gname,gadmin,members):
	newgroup=group(gname,gadmin,members)
	return newgroup
class group:
	def __init__(self,gname,gadmin,members=None):
		self.name=gname
		self.admin=gadmin
		if(members==None):
			self.members=[]
		else:
			self.members=members
		self.members.append(gadmin)
	def append_usr(self,user):
		if(user not in self.members):
			self.members.append(user)
			return True
		return False
	def delete_usr(self,user):
		if(user in self.members):
			self.members.remove(user)
	def send_msg(self,msg):
		for i in self.members:
			i.send_msg(msg)
		

	
def login(user,pwd):
	global users
	for i in users:
		if(i.name==user and i.password==pwd):
			return i
	return False
def register(username,pwd):
	global users
	for i in users:
		if(i.name==user):
			return False
	newuser=user(username,pwd,None,None)
	users.append(newuser)
	return newuser
def thread(socket,address):
	global closelock
	global close
	global users
	global groups
	socket.mysend("OK")
	command=socket.myreceive()
	result=re.match("(R{0,1}USER) ([a-z]*) ([a-z]*) *$",command)
	user=None
	if result is not None:
		(opt,username,pw)=result.groups()
		
		if(opt!="USER" and opt!="RUSER"):
			socket.mysend("BAD COMMAND")
			socket.sock.close()
			return
		
		if(opt=="USER" and login(username,pw)):
			user=login(username,pw)
			msgs=len(user.queue)
			resp="OK ("+str(msgs)+")"
			socket.mysend(resp)
			command=socket.myreceive()
			if(command=="OK"):
				tosend=mysocket()
			
				tosend.connect(address[0], 45000)
			
				user.set_sendsock(tosend)
					
			
		
			
				
		elif(opt=="RUSER"):
			user=register(username,pw)
			if(user!=False):
				msgs=len(user.queue)
				resp="OK ("+str(msgs)+")"
				socket.mysend(resp)
				command=socket.myreceive()
				if(command=="OK"):
					tosend=mysocket()
					
					tosend.connect(address[0], 45000)
					user.set_sendsock(tosend)			
			else:
				socket.mysend("BAD COMMAND: USER ALREADY EXISTS\n")
				socket.sock.close()
				return
		else:
			socket.mysend("BAD COMMAND, INVALID USER OR PASSWORD\n")
			socket.sock.close()
			return
	else:
		socket.mysend("BAD COMMAND")
		socket.sock.close()
		return
	while(True):
	
		
				
		msg=socket.myreceive()
		print msg
		print "\n"
		if(msg==False):
			user.disconnect()
			socket.close()
			return
		split=msg.split(';')
		if(msg=="DISCONNECT"):
			socket.close()
			user.send_msg("DISCONNECT")
			user.disconnect()
			return
		if(len(split)!=3):
			socket.mysend("BAD COMMAND:")
			continue
		
		if(split[0]=="CREATEGROUP"):
			
			gname=split[1]
			if(gname==""):
			
				socket.mysend("BAD COMMAND: INVALID NAME OF GROUP")
				continue
			ngroup=creategroup(gname,user,[])
			addgroup(ngroup)
			socket.mysend("OK")
			continue
		if(split[0]=="APPENDTOGROUP"):
			usrname=split[2]
			groupname=split[1]
			group=None
			for i in groups:
				if i.name==groupname:
					group=i
					break
			if(group==None):
				socket.mysend("BAD COMMAND: INVALID NAME OF GROUP")
				continue					
			newmember=None
			for i in users:
				if(i.name==usrname):
					newmember=i
					break
			if(newmember==None):
				socket.mysend("BAD COMMAND: INVALID NAME OF USER")
				continue
			if(group.append_usr(newmember)):
				socket.mysend("OK")
			else:
				socket.mysend("BAD COMMAND: USER IS IN THE GROUP")
			continue
				
		elif(split[1]=="G"):
			msg=user.name
			msg+=";"+split[0]+";"+split[2]
			sent=send_groupal_msg(msg,split[0])
			if(sent==False):
				socket.mysend("BAD COMMAND: INVALID NAME OF GROUP")
				continue
			socket.mysend("OK")
		elif(split[1]=="S"):
		
			usr=split[0]
			msg=user.name
			msg+=";"+"0;"+split[2]
			pass
			sent=False
			for i in users:
				if(usr==i.name):
					i.send_msg(msg)
					socket.mysend("OK")
					sent=True
					break
			if(sent):
				continue
			socket.mysend("BAD COMMAND: INVALID NAME OF USER")
			continue
		else:
			socket.mysend("BAD COMMAND")
class mysocket:
	global users
	
	def __init__(self, sock=None):
	    if sock is None:
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    else:
		self.sock = sock
	def close(self):
		self.sock.close()
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
	def greet(self):
		msg=self.myreceive()
	'''
f=open("record.txt",'r')
f=f.readlines()
user=None
mode=None
for i in f:
	temp=i.strip()
	result=re.match(" *",temp)
	if(result):
		if(!user):
			users.append(user)
		user=None
		continue
	result=re.match("USERS: *",temp)
	if (result):
		mode='u'
		continue
	if(mode='u'):
		result=re.match("([a-z]*): *")
		
		
		
		
	
	(user,password)=temp.split(' ')
	logins[user]=password
print logins
'''
q1=["user;0;hola","mama;0;hola hijo"]
usr1=user("admin","admin",q1,None)
users.append(usr1)
usr2=user("juan","juan",None,None)
users.append(usr2)
grupo=group("futbol",usr1,[usr2])
groups.append(grupo)
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind(('', 7000))
#become a server socket
serversocket.listen(10)
while(True):
	
	closelock.acquire()
	if(close==1):
		closelock.release()
		break
	closelock.release()	
	(csocket, address) = serversocket.accept()
	clientsocket=mysocket(csocket)
	t=threading.Thread(target=thread,args=(clientsocket,address))
	threads.append(t)
	t.start()




serversocket.close()


