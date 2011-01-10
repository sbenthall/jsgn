#!/usr/bin/env python

"""
basic web handler for JSGN
"""

try:
  import json
except ImportError:
  import simplejson as json

from jsgn import DirectedGraph
from webob import Request, Response, exc

class JSGNHandler(object):
  def __init__(self, filename):
    self.graph = DirectedGraph(filename)

  def __call__(self, environ, start_response):
    request = Request(environ)
    content_type = 'application/json'
    if request.method == 'GET':
      if 'text' in request.GET:
        content_type = 'text/plain'
      res = Response(content_type=content_type,
                      body=self.graph.dump())
    if request.method == 'POST':
      types = {0: 'graph', # /
               1: 'node',  # /node1
               2: 'edge'}  # /node1/node2
      path = request.path_info.strip('/')
      path = path.split('/')
      if path == ['']:
        path = []
      type = types.get(len(path), None)
      if type is None:
        res = exc.HTTPNotFound()
        # TODO set content type, body
        return res(environ, start_response)      
      if request.headers['Content-Type'] == 'application/json':
        import pdb; pdb.set_trace()
        self.graph.save()
      else:
        # normal POST requests can only update metadata on
        # an object
        import pdb; pdb.set_trace()
        self.graph.save()
        res = Response(content_type=content_type,
                       body=self.graph.dump())

    return res(environ, start_response)

if __name__ == '__main__':
  import tempfile
  from wsgiref import simple_server
  app = JSGNHandler(tempfile.mktemp())
  server = simple_server.make_server(host='0.0.0.0', port=8080, app=app)
  server.serve_forever()
