#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer
import os
import socket

from data_uri import DataURI

HOME_DIR = os.environ['HOME']
IMAGE_DIR = os.path.join(
    HOME_DIR, 'Library/Application Support/org.cdglabs.camsketch')


class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/saveImage':
            self._save_image()
        else:
            raise Exception('Unexpected POST request to ' + self.path)

    def _save_image(self):
        content_len = int(self.headers.getheader('content-length'))
        uri = DataURI(self.rfile.read(content_len))
        with open(os.path.join(IMAGE_DIR, 'image.png'), 'wb') as f:
            f.write(uri.data)
        self._send_response(200, 'ok')

    def _send_response(self, code, data):
        self.send_response(code)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)


class CamsketchServer(object):
    def __init__(self):
        # Set the root of the server to the 'frontend' dir.
        # SimpleHTTPRequestHandler will serve GET requests from there.
        root = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '../frontend')
        os.chdir(root)

        if not os.path.exists(IMAGE_DIR):
            os.makedirs(IMAGE_DIR)

        self.port = 8000

        # Try to find an open port anywhere between 8000 and 8080
        self.httpd = None
        for i in xrange(1, 80):
            try:
                self.httpd = SocketServer.TCPServer(("", self.port), Handler)
                break
            except socket.error:
                self.port = self.port + i

        if not self.httpd:
            raise Exception("Could not find an open port")

        hostname = "http://" + socket.gethostbyname(socket.gethostname())
        self.address = hostname + ':' + str(self.port)

    def serve_forever(self):
        print "camsketch is listening at " + self.address
        self.httpd.serve_forever()

    def shutdown(self):
        self.httpd.shutdown()


if __name__ == "__main__":
    try:
        CamsketchServer().serve_forever()
    except KeyboardInterrupt:
        pass
