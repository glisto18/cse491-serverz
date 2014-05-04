#!/usr/bin/env python

import sys
import os
import random
import socket
import time
import urlparse
import StringIO
import argparse

import app
import imageapp
from django.core.wsgi import get_wsgi_application
from wsgiref.validate import validator

import quixote
from quixote.demo.altdemo import create_publisher

_the_app = None
_selected_app = None

def make_app():
    global _the_app
    global _selected_app
    if _the_app is None:
        if _selected_app == 'image':
            imageapp.setup()
            p = imageapp.create_publisher()
            _the_app = quixote.get_wsgi_app()
        elif _selected_app == 'altdemo':
            p = create_publisher()
            _the_app = quixote.get_wsgi_app()
        elif _selected_app == 'myapp':
            _the_app = app.make_app()
        elif _selected_app == 'django':
            sys.path.append(os.path.join(os.path.dirname(__file__), 'imageappdjango'))
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imageappdjango.imageappdjango.settings-prod")
            _the_app = get_wsgi_application()
        else:
            raise Exception("Invalid app selected")
    return _the_app


def getRequest(conn):
    request = ''
    while True:
        if request[-4:] == '\r\n\r\n':
            break
        request += conn.recv(1)

    return request

def handle_connection(conn):
    def start_response(status, response_headers, exc_info=None):
        if exc_info:
            try:
                raise exc_info[1].with_traceback(exc_info[2])
            finally:
                exc_info = None

        conn.send('HTTP/1.0 %s\r\n' % status)

        for header in response_headers:
            key, value = header
            conn.send('%s: %s\r\n' % (key,value))
        conn.send('\r\n')

    environ = {}
    environ['REQUEST_METHOD'] = ''
    environ['PATH_INFO'] = ''
    environ['SERVER_PROTOCOL'] = ''
    environ['SCRIPT_NAME'] = ''
    environ['wsgi.input'] = StringIO.StringIO('')
    environ['QUERY_STRING'] = ''
    environ['CONTENT_LENGTH'] = '0'
    environ['CONTENT_TYPE'] = 'text/html'
    environ['SERVER_NAME'] = "%s" % conn.getsockname()[0]
    environ['SERVER_PORT'] = "%s" % conn.getsockname()[1]
    environ['wsgi.version'] = (1,0)
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.multithread'] = 0
    environ['wsgi.multiprocess'] = 0
    environ['wsgi.run_once'] = 0
    environ['wsgi.url_scheme'] = 'http'

    request = getRequest(conn)
    if request != '':
        request_line, headers_string = request.split('\r\n', 1)
        environ['REQUEST_METHOD'], path, \
          environ['SERVER_PROTOCOL'] = request_line.split(' ')

        path = urlparse.urlparse(path)
        environ['PATH_INFO'] = path.path
        environ['QUERY_STRING'] = path.query

        if headers_string != '' and headers_string != '\r\n':
            headers = []
            headers = headers_string.split('\r\n')
            headersDictionary = {}

            for line in headers:
                if line != '':
                    k, v = line.split(': ', 1)
                    headersDictionary[k.lower()] = v

            if 'content-length' in headersDictionary.keys():
                environ['CONTENT_LENGTH'] = headersDictionary['content-length']

            if int(environ['CONTENT_LENGTH']) != 0:
                environ['wsgi.input'] = StringIO.StringIO(conn.recv(int(environ['CONTENT_LENGTH'])))

            if 'content-type' in headersDictionary.keys():
                environ['CONTENT_TYPE'] = headersDictionary['content-type']

            if 'cookie' in headersDictionary.keys():
                environ['HTTP_COOKIE'] = headersDictionary['cookie']

    wsgi_app = make_app()
    validator_app = validator(wsgi_app)
    result = wsgi_app(environ, start_response)

    for obj in result:
        conn.send(obj)

    result.close()
    conn.close()

def main(socketmodule = None):
    if socketmodule == None:
        socketmodule = socket

    global _selected_app

    parser = argparse.ArgumentParser(description='Parse arguments for the apps')
    parser.add_argument('-A', dest='application', nargs=1, choices=['image','altdemo','myapp','django'], required=True)
    parser.add_argument('-p', dest='port', type=int, nargs=1)
    args = parser.parse_args()
    if not args.port:
        port = random.randint(8000,9999)
    else:
        port = args.port[0]

    _selected_app = args.application[0]

    s = socketmodule.socket()
    host = socketmodule.getfqdn()
    s.bind((host,port))

    print 'Start server on', host, port
    print 'The server URL for this application would be http://%s:%s/' % (host,port)

    s.listen(5)

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        c, (client_host, client_port) = s.accept()
        print 'Receiving connection from', client_host, client_port
        handle_connection(c)

if __name__ == '__main__':
    main()
