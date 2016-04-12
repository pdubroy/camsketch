#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer
import os
import socket

from data_uri import DataURI

IMAGE_DIR = os.path.join(
    os.environ['HOME'], 'Library/Application Support/org.cdglabs.camsketch')


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

if __name__ == "__main__":
  # Set the root of the server to the 'frontend' dir.
  root = os.path.join(
      os.path.dirname(os.path.abspath(__file__)), '../frontend')
  os.chdir(root)

  port = 8000

  # Try to find an open port anywhere between 8000 and 8080
  httpd = None
  for i in xrange(1, 80):
    try:
      httpd = SocketServer.TCPServer(("", port), Handler)
      break
    except socket.error:
      port = port + i

  if httpd:
    server = "http://" + socket.gethostbyname(socket.gethostname())
    print "camsketch is listening at " + server + ':' + str(port)
    try:
      httpd.serve_forever()
    except KeyboardInterrupt:
      pass
