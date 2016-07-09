import socket


def recv_del(sock,delim):
	string = ""
	while True:
		char = sock.recv(1)
		if char != delim:
			string += char
		else:
			return string


s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(("gmail.com",80))

THIS_NODE = s.getsockname()[0]
MASTER_NODE = '192.168.1.95'
PORT = 2000
WEB_PORT = 2001

s.close()

#Define ourself as a web server
browser_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
browser_socket.bind((THIS_NODE,WEB_PORT))
browser_socket.listen(1)

#Define connection to master server
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect((MASTER_NODE,PORT))

#Handshake
print "Connected"
server.sendall("NewConnexion: 192.168.1.95")#Address to direct to this node
server.recv(28)
server.sendall("Got it bro")

while True:
	#Wait for request
	print "Waiting for request from master..."
	target = recv_del(server,'$')
	print "Recieved request for %s"%target
	server.sendall("Sure am, put me through!")

	#Serve HTML document
	print "Waiting for HTTP connection..."
	(browser,addr) = browser_socket.accept()
	http_request = browser.recv(1024)
	browser.sendall('''HTTP/1.1 200 OK

Hello, World!''')
	browser.close()
	print "Request has been served\n"