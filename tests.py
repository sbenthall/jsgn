from jsgn import *
import json

jsgn_dict = {
    'structure' : {
        'node1' : {
            'node2' : { 'edge-key': 12},
            'node3' : { 'edge-key': 13}
            },
        'node2' : {
            'node3' : { 'edge-key':23}
            },
        'node3' : {}
        },
    'nodes' : {
        'node1': { 'node-key' : 1},
        'node2': { 'node-key' : 2},
        'node3': { 'node-key' : 3}
        }
    }

graph1 = Graph(jsgn_dict)


node1 = graph1.get_node('node1')

assert(node1.metadata['node-key'] == 1)

assert(node1.get_edge('node2').metadata == graph1.get_edge('node1','node2').metadata)

node4 = graph1.add_node('node4', {'node-key': 4})
assert(node1.add_edge('node4', {'edge-key':14}).to_node.metadata['node-key'] == 4)

assert(node4.add_edge('node1').from_node.metadata == node4.metadata)

node4.get_edge('node1').metadata['edge-key'] = 41
assert(graph1.get_edge('node4','node1').metadata['edge-key'] == 41)

assert(len(node1.children()) == 3)
