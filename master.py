import socket

THIS_SERVER = '192.168.1.95'
PORT = 2000
WEB_PORT = 2001

sckt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sckt.bind((THIS_SERVER,PORT))
sckt.listen(5)

#Keeps a list of all nodes and their addresses, updated every so often. Nodes are moved to the bottom of the list after a connection attempt is made - either it doesn't respond, and it isn't up, so it isn't worth trying for a while, or it is up but in use, so it isn't worth trying for a while
nodes = {}

while True:
	#Ready to recv connection from client
	print "Waiting for connection..."
	(client,addr) = sckt.accept()
	print "Connection from "+str(addr[0])+" on port "+str(addr[1])

	request = client.recv(1024).split()

	if request[0] == "NewConnexion:": #If it is a node, refresh the node list with the new list of websites the node hosts
		print "It's a node authentication! Refreshing node list..."
		for key in nodes:
			if (client,addr) in nodes[key]:
				nodes[key].remove((client,addr))
		for site in request[1:]:
			if site not in nodes:
				nodes[site] = []
			nodes[site].append((client,addr))

		print "Waiting for handshake..."
		client.sendall("Okay cool wait for a request")
		client.recv(10)
		print "Node "+str(addr[1])+" ready"

	else: #If it is a client, select a node and ask it if it is up
		print "It's an HTTP request! Selecting the right node..."
		target = request[4].split(':')[0]
		response = ""
		while response == "":
			nodes[target][0][0].send(target+'$')
			response = nodes[target][0][0].recv(24)
			if response == "":
				nodes[target][0][0].close()
				nodes[target].pop(0)

		#If there is a response, redirect client to that node
		print "Sending redirect..."
		destination = nodes[target][0][1][0]
		http_response = """HTTP/1.1 301 Moved Permanently
Location: http://%s:%d/
"""%(destination,WEB_PORT)

		client.sendall(http_response)
		client.close()

		nodes[target].append(nodes[target].pop(0))

	print ''