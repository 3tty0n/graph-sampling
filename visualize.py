# coding=utf-8

import matplotlib.pyplot as plt
import networkx as nx
import json
import seaborn as sns


G = nx.Graph()
G.add_edges_from([(1, 2), (2, 3), (3, 4), (1, 3), (1, 4)], color='blue')


def save(G, name):
    json.dump(dict(nodes=[[n, G.node[n]] for n in G.nodes()],
                   edges=[[u, v, G.edge[u][v]] for u, v in G.edges()]),
              open(name, 'w'), indent=2)


def load(name):
    G = nx.DiGraph()
    d = json.load(open(name))
    G.add_nodes_from(d['nodes'])
    G.add_edges_from(d['edges'])
    return G
