import json
import os.path

def open_graph(file_name):
    file = open(file_name,"r")
    graph_dict = json.loads(file.read())
    return Graph(graph_dict)

def save_graph(file_name):
    file = open(self.file_name,"w")
    file.write(self.dump())
    file.close()
    
class Graph():
    ''' A dict that contains the edge structure indexed by nodes'''
    structure = {}
    ''' A dict that contains metadata on nodes '''
    nodes = {}

    def __init__(self,graph_dict=None):        
        if graph_dict is not None:
            self.structure = graph_dict.get('structure',{})
            self.nodes = graph_dict.get('nodes',{})
        
    def dump(self):
        return json.dumps(
            {
                'structure' : self.structure,
                'nodes' : self.nodes
                }
            )

    def add_node(self, node, metadata={}):
        '''
        Adds a node.
        WARNING: Overwrites a node.
        '''
        self.structure[node] = {}
        self.nodes[node] = metadata
        return self.get_node(node)
           
    def has_node(self, node):
        return self.nodes.get(node) is not None
                
    def get_node(self, node):
        return Node(node, self)

    def get_edge(self, from_node, to_node):
        return Edge(from_node, to_node, self)

class Node():
    metadata = {}
    edges = {}
    graph = None
    id = ""

    def __init__(self, node, graph):
        self.edges = graph.structure[node]
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

class Edge():
    from_node = None
    to_node = None                
    metadata = {}
    graph = None

    def __init__(self, from_node, to_node, graph):
        self.from_node = graph.get_node(from_node)
        self.to_node = graph.get_node(to_node)
        self.metadata = graph.structure[from_node][to_node]
        self.graph = graph
