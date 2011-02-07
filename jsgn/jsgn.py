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
    return DirectedGraph(graph_dict)

def save_graph(graph, file_name):
    file = open(file_name,"w")
    file.write(graph.dump())
    file.close()


class DirectedGraph(object):
    graph = {
        'nodes' : {},
        'edges' : {}
        }

    def __init__(self, graph_dict=None):
        if graph_dict is not None:
            self.graph = graph_dict
            self.edges = graph_dict.get('edges',{})
            self.nodes = graph_dict.get('nodes',{})
        # convenience attrs
        self.nodes = self.graph['nodes']
        self.edges = self.graph['edges']

    ### functions for loading/saving

    def as_dict(self):
        return self.graph

    def load(self, jsongraph):
        ## should homogenize 'load' and 'save' to
        ## be file or dict loading
        self.graph = json.loads(jsongraph)
        self.nodes = self.graph['nodes']
        self.edges = self.graph['edges']

    def dump(self):
        return json.dumps(self.graph)
        
    def save(self, filename):
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
        self.edges.setdefault(node, {})
        return self.get_node(node)

    def add_edge(self, node1, node2, **metadata):
        self.edges.setdefault(node1, {}).setdefault(node2, {}).update(metadata)
        self.add_node(node1)
        self.add_node(node2)


    ### Object Graphical Mapping
                
    def get_node(self, node):
        return Node(node, self)

    def get_edge(self, from_node, to_node):
        return Edge(from_node, to_node, self)


    ### functions for graph access

           
    def has_node(self, node):
        return self.nodes.get(node) is not None

    def __iter__(self):
        """iterate over edges"""
        for node1, value in self.edges.items():
            for node2, metadata in value.items():
                yield node1, node2, metadata


class Node():
    metadata = {}
    edges = {}
    graph = None
    id = ""

    def __init__(self, node, graph):
        self.edges = graph.edges[node]
        self.metadata = graph.nodes[node]
        self.graph = graph
        self.id = node

    def get_edge(self, to_node):
        return Edge(self.id, to_node,self.graph)

    def add_edge(self, to_node, metadata={}):
        if not self.graph.has_node(to_node):
            self.graph.add_node(to_node)
        self.edges[to_node] = metadata
        return self.get_edge(to_node)

    def children(self):
        ## should return an iterator
        return [Node(node,self.graph) for node in self.edges.keys()]

class Edge():
    from_node = None
    to_node = None                
    metadata = {}
    graph = None

    def __init__(self, from_node, to_node, graph):
        self.from_node = graph.get_node(from_node)
        self.to_node = graph.get_node(to_node)
        self.metadata = graph.edges[from_node][to_node]
        self.graph = graph



if __name__ == '__main__':
    # illustrate basic functionality
    graph = DirectedGraph()
    graph.add_edge('foo', 'bar', **{'count': 2})
    graph.add_edge('foo', 'fleem', **{'count': 7})
    graph.add_node('fleem', **{'description' :'a serious fleem'})
    assert graph.edges == {'fleem': {},'foo': {'bar': {'count': 2}, 'fleem': {'count': 7} }, 'bar' :{} }
    assert graph.nodes['fleem']['description'] == 'a serious fleem'

    count = sum([sum([j.get('count', 0) for j in i.values()]) for i in graph.edges.values()])
    assert count == 9

    # iterate over edges
    for node1, node2, metadata in graph:
        print '%s -> %s : %s' % (node1, node2, metadata)

    assert sum([j[2].get('count', 0) for j in graph]) == 9

