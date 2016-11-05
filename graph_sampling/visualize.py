# coding=utf-8

import json
import networkx as nx
from networkx.readwrite import json_graph
import util
import flask

G = nx.read_edgelist('data/input/twitter_combined.txt')
# this d3 example uses the name attribute for the mouse-hover value,
# so add a name to each node
edges = list(util.random_walk(graph=G, size=1000, metropolized=True))
G1 = nx.Graph()
G1.add_path(edges)
for n in G1:
    G1.node[n]['name'] = n
# write json formatted data
d = json_graph.node_link_data(G1) # node-link format to serialize
# write json
json.dump(d, open('graph_sampling/visualize/visualize.json','w'))
print('Wrote node-link JSON data to visualize/visualize.json')

# Serve the file over http to allow for cross origin requests
app = flask.Flask(__name__, static_folder=".")

@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)
print('\nGo to http://localhost:8000/visualize.html to see the example\n')
app.run(port=8000)