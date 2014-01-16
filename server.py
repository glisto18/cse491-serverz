#!/usr/bin/env python
import random
import socket
import time

s = socket.socket()         # Create a socket object
host = socket.getfqdn() # Get local machine name
port = random.randint(8000, 9999)
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port
print 'The Web server URL for this would be http://%s:%d/' % (host, port)

s.listen(5)                 # Now wait for client connection.

print 'Entering infinite loop; hit CTRL-C to exit'
while True:
    # Establish connection with client.    
    c, (client_host, client_port) = s.accept()
    print c.recv(1000)
    print 'Got connection from', client_host, client_port
    c.send('HTTP/1.0 200 OK\nDate: ' + time.asctime(time.gmtime()) + '\nContent-Type: text/html\n\n<html>\n<head>\n<title>Brians Web Server</title>\n</head>\n<body>\n<h1>Hello, world</h1> this is Brian\'s web server\n</body>\n</html>\n')
    c.close()
