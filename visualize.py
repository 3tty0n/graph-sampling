# coding=utf-8

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
import json
from networkx.readwrite import json_graph


G = nx.Graph()
G.add_edges_from([(1, 2), (2, 3), (3, 4), (1, 3), (1, 4)])


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

nx.write_gexf(G, 'test.gexf')