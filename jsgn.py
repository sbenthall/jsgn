import json
import os.path


class Graph():
    graph = {}
    file_name = None

    def __init__(self,file_name):
        if os.path.isfile(file_name):
            file = open(file_name,"r")
            self.graph = json.loads(file.read())
        self.file_name = file_name

    def dump(self):
        return json.dumps(self.graph)
        
    def save(self):
        if self.file_name:
            file = open(self.file_name,"w")
            file.write(self.dump())
            file.close()

    def add_node(self, node):
        '''
        Adds a node.
        WARNING: Overwrites a node.
        '''
        self.graph[node] = {}

    def add_edge(self, node1, node2, metadata):
        self.graph[node1][node2] = metadata

