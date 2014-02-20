import sys
import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
<<<<<<< HEAD
=======
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
		      '<html><body>' + \
                      '<h1>Hello, world.</h1>' + \
                      "This is romanda1's Web server written by J. Rucinski. <BR>" + \
		      "<A HREF='/content'>Content</A><BR>" + \
		      "<A HREF='/file'>File</A><BR>" + \
		      "<A HREF='/image'>Image</A>" + \
		      '</html></body>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Content Page</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>File Page</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Image Page</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_post():
    conn = FakeConnection("POST /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello, world.</h1>' + \
		      "This is romanda1's Web server written by J. Rucinski. \r\n" + \
		      'This is a POST.'
>>>>>>> f0618a0f39c17ced66537faaa83dcdc0997a32f0

    server.handle_connection(conn)

    assert 'HTTP/1.0 200 OK\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<h1>Welcome to Brian\'s Web Server</h1>' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)


def test_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0 200 OK\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<h1>Content page!</h1>' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0 200 OK\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<h1>File page!</h1>' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0 200 OK\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<h1>Image page!</h1>' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_post():
    conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0 404 NOT FOUND\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<h1>404 NOT FOUND</h1>' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_form_get():
    conn = FakeConnection("GET /submit?firstname=Brian&lastname=Jurgess HTTP/1.0\r\n\r\n")

    
    server.handle_connection(conn)

    assert 'HTTP/1.0 200 OK\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert 'Hello Brian Jurgess.' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_form_post():
    conn = FakeConnection("POST /submitpost HTTP/1.0\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 32\r\n\r\nfirstname=Brian&lastname=Jurgess")

    server.handle_connection(conn)

    assert 'HTTP/1.0 200 OK\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert 'Hello Brian Jurgess.' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_form_page_get():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0 200 OK\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<form action="/submit" method="GET">' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_form_page_post():
    conn = FakeConnection("GET /formpost HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0 200 OK\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<form action="/submitpost" method="POST">' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_501_error():
    conn = FakeConnection("PATCH / HTTP/1.1\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0 501 Not Implemented\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<h1>ERROR 501 NOT IMPLEMENTED</h1>' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_404_error():
    conn = FakeConnection("GET /blah HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0 404 NOT FOUND\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<h1>404 NOT FOUND</h1>' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_multipart_form():
    request = 'POST / HTTP/1.0\r\nContent-type: multipart/form-data; boundary=aaaa\r\n\r\n' + \
              '--aaaa' + \
              '--aaaa'
    conn = FakeConnection(request)

    server.handle_connection(conn)

    assert 'HTTP/1.0 404 NOT FOUND' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<h1>404 NOT FOUND</h1>' in conn.sent, 'Got: %s' % (repr(conn.send),)
