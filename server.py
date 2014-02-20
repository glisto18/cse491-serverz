#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
import StringIO
import jinja2
import sys
from app import make_app
import time

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
# Set up the loader and environment
# for jinja2 templating engine
loader = jinja2.FileSystemLoader('./templates')
env = jinja2.Environment(loader=loader)
=======
def createEnviron(conn):
    environ = {}
>>>>>>> c3b3629ce9159a70e1006468c33619b4233ed1df

    request = ''
    while True:
        recv_value = conn.recv(1)
        request += recv_value
        if '\r\n\r\n' in request:
            break

    request_headers, request_body = request.split('\r\n\r\n')

    try:
        request_line, headers_string = request_headers.split('\r\n', 1)
    except:
        environ['REQUEST_METHOD'], PATH,\
        environ['SERVER_PROTOCOL'] = request_headers.split(' ')
        PATH = urlparse.urlparse(PATH)
        environ['PATH_INFO'] = PATH.path
        environ['QUERY_STRING'] = PATH.query

        return environ

    environ['REQUEST_METHOD'], PATH, \
    environ['SERVER_PROTOCOL'] = request_line.split(' ')

    PATH = urlparse.urlparse(PATH)

    environ['PATH_INFO'] = PATH.path
    environ['QUERY_STRING'] = PATH.query

    headers = headers_string.split('\r\n')

    headerDict = {}
    for line in headers:
        k, v = line.split(': ', 1)
        headerDict[k.lower()] = v

    if 'content-length' in headerDict.keys():
        environ['CONTENT_LENGTH'] = int(headerDict['content-length'])
        environ['wsgi.input'] = StringIO.StringIO(conn.recv(int(headerDict['content-length'])))

    if 'content-type' in headerDict.keys():
        environ['CONTENT_TYPE'] = headerDict['content-type']    

    return environ






def handle_connection(conn):
    # Get the request and split it to get the
    # request type and the requested folder
    headers_set = []
    headers_sent = []

    def write(data):
        out = StringIO.StringIO()

        if not headers_set:
            raise AssertionError("write() called before start_response()")
        elif not headers_sent:
            status, response_headers = headers_sent[:] = headers_set
            out.write('HTTP/1.0 %s\r\n' % status)
            for header in response_headers:
                out.write('%s: %s\r\n' % header)
            out.write('\r\n')

        out.write(data)
        conn.send(out.getvalue())

    def start_response(status, response_headers, exc_info=None):
        if exc_info:
            try:
                if headers_sent:
                    raise exc_info[1].with_traceback(exc_info[2])
            finally:
                exc_info = None
        elif headers_set:
            raise AssertionError("Headers already set!")

        headers_set[:] = [status, response_headers]
        headers_set[1].append(('Date', time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())))
        
        return write

    wsgi_app = make_app()
    environ = createEnviron(conn)
    result = wsgi_app(environ, start_response)

    try:
        if result:
            write(result)
        if not headers_sent:
            write('')
    finally:
        conn.close()




    # request_temp = ''
    # while True:
    #     request_temp += conn.recv(1)
    #     if '\r\n\r\n' in request_temp:
    #         break

    # request = StringIO.StringIO(request_temp)
    # environ = {}

    # environ['REQUEST_METHOD'], path, \
    # environ['SERVER_PROTOCOL'] = request.readline().split()

    # # Get the path information
    # path = urlparse.urlparse(path)
    # environ['PATH_INFO'] = path.path
    # environ['QUERY_STRING'] = path.query

    # # Get the query string information
    # if environ['REQUEST_METHOD'] == 'GET':
    #     GetRequests(conn, environ, request)
    # elif environ['REQUEST_METHOD'] == 'POST':
    #     PostRequests(conn, environ, request)
    # else:
    #     error_500_not_implemented(conn, environ)

    # conn.close()

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
        print 'Got connection from', client_host, client_port
        handle_connection(c)

if __name__ == '__main__':
    main()
=======
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

=======
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

>>>>>>> f0618a0f39c17ced66537faaa83dcdc0997a32f0
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
               "This is romanda1's Web server written by J. Rucinski. <BR>" + \
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
	   "This is romanda1's Web server written by J. Rucinski. \r\n" + \
	   'This is a POST.')

if __name__== '__main__':
	main()
<<<<<<< HEAD
>>>>>>> f0618a0f39c17ced66537faaa83dcdc0997a32f0
=======
>>>>>>> f0618a0f39c17ced66537faaa83dcdc0997a32f0
