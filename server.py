#!/usr/bin/env python
import random
import socket
import time

def main():
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
	handle_connection(c)

        print 'Got connection from', client_host, client_port

def handle_connection(c):
    req = c.recv(1000)
    req = req.split(' ')
    reqType = req[0]
    path = req[1]
    if reqType == 'GET':
        handle_get(c,path)
    elif reqType == 'POST':
        handle_post(c)
    c.close()

def handle_get(c,path):	   
    # send a response
    #if main directory
    if path == '/':
        c.send('HTTP/1.0 200 OK\r\n' + \
               'Content-type: text/html\r\n' + \
               '\r\n')
	c.send('<html><body>' + \
               '<h1>Hello, world.</h1>' + \
               "This is rucins11's Web server.<BR>" + \
	       "<A HREF='/content'>Content</A><BR>" + \
               "<A HREF='/file'>File</A><BR>" + \
	       "<A HREF='/image'>Image</A>" + \
	       '</html></body>')

    #if content directory
    elif path == '/content':
        c.send('HTTP/1.0 200 OK\r\n' + \
               'Content-type: text/html\r\n' + \
	       '\r\n' + \
	       '<h1>Content Page</h1>')
    #if file directory
    elif path == '/file':
        c.send('HTTP/1.0 200 OK\r\n' + \
               'Content-type: text/html\r\n' + \
	       '\r\n' + \
	       '<h1>File Page</h1>')
    #if image directory
    elif path == '/image':
        c.send('HTTP/1.0 200 OK\r\n' + \
               'Content-type: text/html\r\n' + \
	       '\r\n' + \
	       '<h1>Image Page</h1>')

def handle_post(c):
    c.send('HTTP/1.0 200 OK\r\n' + \
           'Content-type: text/html\r\n' + \
	   '\r\n' + \
	   '<h1>Hello, world.</h1>' + \
	   "This is rucins11's Web server. \r\n" + \
	   'This is a POST.')

if __name__== '__main__':
	main()
