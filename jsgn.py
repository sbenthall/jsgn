import json
import os


class DirectedGraph(object):

    def __init__(self, filename):
        if filename and os.path.isfile(filename):
            f = open(filename,"r")
            self.graph = json.loads(f.read())
        else:
            self.graph = {'nodes': {}, 'edges': {}}
        self.filename = filename

        # conveniences
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

if __name__ == '__main__':
    graph = DirectedGraph(None)
    graph.add_edge('foo', 'bar', **{'count': 2})
    graph.add_edge('foo', 'fleem', **{'count': 7})
    graph.add_node('fleem', description='a serious fleem')

    assert graph.edges == {'foo': {'bar': {'count': 2}, 'fleem': {'count': 7} } }
    assert graph.nodes['fleem']['description'] == 'a serious fleem'

    count = sum([sum([j.get('count', 0) for j in i.values()]) for i in graph.edges.values()])
    assert count == 9
