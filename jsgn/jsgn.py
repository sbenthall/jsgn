"""
basic directed graph API
"""

import os
try:
    import json
except ImportError:
    import simplejson as json

def open_graph(file_name):
    file = open(file_name,"r")
    graph_dict = json.loads(file.read())
    return Graph(graph_dict)

def save_graph(graph, file_name):
    file = open(file_name,"w")
    file.write(graph.dump())
    file.close()


class DirectedGraph(object):

    graph = {}

    def __init__(self, graph_dict=None):
        if graph_dict is not None:
            self.edges = graph_dict.get('edges',{})
            self.nodes = graph_dict.get('nodes',{})
        # convenience attrs
        self.nodes = self.graph['nodes']
        self.edges = self.graph['edges']

    ### functions for loading/saving

    def load(self, jsongraph):
        self.graph = json.loads(jsongraph)

    def dump(self):
        return json.dumps(self.graph)
        
    def save(self):
        if self.filename:
            file = open(self.filename,"w")
            file.write(self.dump())
            file.close()

    ### functions for updating graph

    def update(self, graph):
        """update the entire graph"""
        if isinstance(graph, DirectedGraph):
            graph = graph.graph

        # update graph metadata
        graphmetadata = dict([(i,j) for i, j in graph.items()
                              if i not in ['nodes', 'edges']])
        self.graph.update(graphmetadata)

        # update nodes
        for node, metadata in graph.get('nodes', {}):
            # TODO: assert metadata is a dict
            self.add_node(node, metadata)

        # update edges
        # TODO

    def add_node(self, node, **metadata):
        self.nodes.setdefault(node, {}).update(metadata)

    def add_edge(self, node1, node2, **metadata):
        self.edges.setdefault(node1, {}).setdefault(node2, {}).update(metadata)
        self.add_node(node1)
        self.add_node(node2)


    ### functions for graph access

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

