# coding=utf-8

import networkx as nx
import numpy as np
import random
import itertools
from util import normalized_mean_square_error


def random_walk_proposal(graph, start_node=None, size=-1):
    """
    提案手法のランダムウォーク
    :param graph:
    :param start_node:
    :param size:
    :return:
    """
    if start_node is None:
        start_node = random.choice(graph.nodes())
    v = start_node
    for c in itertools.count():
        if c == size:
            return
        candidate = random.choice(graph.neighbors(v))
        neighbors_degree = sum(list(map(lambda x: graph.degree(x), graph.neighbors(v))))
        v = candidate if (random.random() < float(graph.degree(v) ** 2 / neighbors_degree)) else v
        yield v


def random_walk_proposal_aggregation(graph, start_node=None, size=-1, tv=1.0, n=100):
    """
    提案手法のランダムウォークを用いてCluster Coefficientを計算する
    :param graph:
    :param start_node:
    :param size:
    :param tv:
    :return:
    """
    result = []
    for i in range(1, n):
        nodes = list(random_walk_proposal(graph, start_node, size))
        data = []
        for node in nodes:
            data.append(nx.clustering(graph, node))
        average = sum(data) / len(data)
        result.append(average)
    ndata = np.array(result)
    naverage = np.average(ndata)
    var = np.var(ndata)
    nmse = normalized_mean_square_error(n, tv, result)
    return {"average": naverage, "var": var, "nmse": nmse}


if __name__ == '__main__':
    G = nx.read_edgelist('data/input/com-amazon.ungraph.txt')
    print(random_walk_proposal_aggregation(graph=G, size=2000, tv=0.3967, n=100))