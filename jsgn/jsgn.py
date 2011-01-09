try:
    import json
except ImportError:
    import simplejson as json
import os

class DirectedGraph(object):

    def __init__(self, filename=None):
        if filename and os.path.isfile(filename):
            f = open(filename,"r")
            self.graph = json.loads(f.read())
        else:
            self.graph = {'nodes': {}, 'edges': {} }
        self.filename = filename

        # convenience attrs
        self.nodes = self.graph['nodes']
        self.edges = self.graph['edges']


    def dump(self):
        return json.dumps(self.graph)
        
    def save(self):
        if self.filename:
            file = open(self.filename,"w")
            file.write(self.dump())
            file.close()

    def add_node(self, node, **metadata):
        self.nodes.setdefault(node, {}).update(metadata)

    def add_edge(self, node1, node2, **metadata):
        self.edges.setdefault(node1, {}).setdefault(node2, {}).update(metadata)
        self.add_node(node1)
        self.add_node(node2)

    def __iter__(self):
        """iterate over edges"""
        for node1, value in self.edges.items():
            for node2, metadata in value.items():
                yield node1, node2, metadata

if __name__ == '__main__':
    # illustrate basic functionality
    graph = DirectedGraph()
    graph.add_edge('foo', 'bar', **{'count': 2})
    graph.add_edge('foo', 'fleem', **{'count': 7})
    graph.add_node('fleem', description='a serious fleem')

    assert graph.edges == {'foo': {'bar': {'count': 2}, 'fleem': {'count': 7} } }
    assert graph.nodes['fleem']['description'] == 'a serious fleem'

    count = sum([sum([j.get('count', 0) for j in i.values()]) for i in graph.edges.values()])
    assert count == 9

    # iterate over edges
    for node1, node2, metadata in graph:
        print '%s -> %s : %s' % (node1, node2, metadata)

    assert sum([j[2].get('count', 0) for j in graph]) == 9

