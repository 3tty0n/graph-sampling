# coding=utf-8

from networkx.readwrite import json_graph

import graphSampling as gs
import networkx as nx
import matplotlib.pyplot as plt


def ba10000_show():
    """
    BA10000.txtを読み込んでグラフを表示する
    :return:
    """
    G = nx.read_edgelist("../data/input/BA10000.txt", nodetype=int)
    pos = {}
    nx.draw(G, pos)
    plt.savefig("../data/output/test_graph.png")
    plt.show()


def twitter_sampling():
    G = nx.read_edgelist("../data/input/twitter_combined.txt", nodetype=int)
    print(gs.cluster_coefficient_average(G))
    print(gs.random_walk_sampling_cca(graph=G, size=100000, metropolized=True))
    print(gs.random_walk_aggregation(graph=G, size=10000, metropolized=True))


def youtube_sampling():
    G = nx.read_edgelist("../data/input/com-youtube.ungraph.txt", nodetype=int)
    print(gs.random_walk_sampling_cca(graph=G, size=10000))
    print(gs.random_walk_aggregation(graph=G, size=10000, metropolized=False))


def youtube_sampling_show(size):
    G = nx.read_edgelist("../data/input/com-youtube.ungraph.txt", nodetype=int)
    nodes = list(gs.random_walk(graph=G, size=size))
    graph = nx.Graph()
    graph.add_path(nodes)
    nx.draw_random(G=graph)
    plt.savefig("../data/output/com-youtube.ungraph.rw." + str(size) + ".png")
    plt.show()


def amazon_sampling():
    G = nx.read_edgelist("../data/input/com-amazon.ungraph.txt")
    graph = nx.Graph()
    nodes = gs.random_walk(graph=G, size=10000)
    graph.add_path(nodes)
    json_graph.node_link_data(graph)
    plt.savefig("../data/output/com-amazon.ungraph.rw.png")
    plt.show()


def sampling():
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (4, 7), (4, 8), (5, 9), (5, 10), (7, 11), (7, 12)])
    print(gs.cluster_coefficient_node(G, 2))
    print(gs.average_degree(G))
    print(list(gs.random_walk(graph=G, size=10)))


if __name__ == "__main__":
    sampling()
