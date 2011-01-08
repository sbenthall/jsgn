from jsgn import Graph
from webob import Request, Response, exc

class JSGNHandler(object):
  def __init__(self, filename):
    self.graph = Graph(filename)

  def __call__(self, environ, start_response):
    request = Request(environ)
    content_type = 'application/json'
    if request.method == 'GET':
      if 'text' in request.GET:
        content_type = 'text/plain'
      return Response(content_type=content_type,
                      body=self.graph.dump())
    if request.method == 'POST':
      import pdb; pdb.set_trace()
      raise NotImplementedError
