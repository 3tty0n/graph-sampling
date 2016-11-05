# coding=utf-8

from typing import *

import itertools
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random


def complete_graph(n) -> nx.Graph:
    """
    完全グラフを計算する

    :param n: ノードの数
    :return: グラフ
    """
    G = nx.Graph()
    if n > 1:
        if G.is_directed():
            edges = itertools.permutations(range(n), 2)
        else:
            edges = itertools.combinations(range(n), 2)
        G.add_edges_from(edges)
    return G


def complete_graph_show(graph, n):
    """
    完全グラフを表示する

    :param graph: グラフ
    :param n: ノードの数
    :return:
    """
    G = graph.complete_graph(n)
    pos = nx.circular_layout(G)
    nx.draw_networkx(G, pos)
    plt.show()


def cluster_coefficient_node(graph, v) -> float:
    """
    graphのあるノードvのクラスタ係数を求める

    :param graph: グラフ
    :param v: ノード
    :return:
    """
    return nx.clustering(graph, v)


def cluster_coefficient_average(graph) -> float:
    """
    graphの平均クラスタ係数を求める
    :param graph: グラフ
    :return: 平均クラスタ係数
    """
    return nx.average_clustering(graph)


def average_degree(graph) -> float:
    """
    graphの平均次数を求める
    :param graph: グラフ
    :return: 平均次数
    """
    values = graph.degree().values()
    return sum(values) / len(values)


def bfs(graph, start, end) -> List[int]:
    """
    graphを幅優先探索する

    :param graph: グラフ
    :param start: 始点ノード
    :param end: 終点ノード
    :return: 訪れたノード列
    """
    graph_successors = nx.bfs_successors(graph, start)

    queue = [start]
    visited = []

    while len(queue) > 0:
        v = queue.pop(0)

        if v == end:
            visited.append(v)
            return visited

        if v not in visited:
            visited.append(v)
            queue += [x for x in graph_successors.get(v, []) if x not in visited]

    return visited


def random_walk(graph, start_node=None, size=-1, metropolized=False) -> List[int]:
    """
    RWでサンプリングしたノード列を返す

    :param graph: グラフ
    :param start_node: 先頭ノード
    :param size: ノード列のサイズ
    :param metropolized: metropolis hasting random walk フラグ
    :return: サンプリングしたノード列
    """
    if start_node is None:
        start_node = random.choice(graph.nodes())

    v = start_node
    for c in itertools.count():
        if c == size:
            return
        if metropolized:
            candidate = random.choice(graph.neighbors(v))
            v = candidate if (random.random() < float(graph.degree(v)) / graph.degree(candidate)) else v
        else:
            v = random.choice(graph.neighbors(v))

        yield v


def random_walk_sampling_cca(graph, start_node=None, size=-1, metropolized=False) -> List[int]:
    """
    RWでサンプリングしたグラフの平均クラスタ係数を返す

    :param graph: グラフ
    :param start_node: 先頭ノード
    :param size: サイズ
    :param metropolized: metropolis hasting random walk フラグ
    :return: 平均クラスタ係数
    """
    if start_node is None:
        start_node = random.choice(graph.nodes())

    nodes = list(random_walk(graph=graph, start_node=start_node, size=size, metropolized=metropolized))

    graph = nx.Graph()
    graph.add_path(nodes=nodes)

    return cluster_coefficient_average(graph)


def random_walk_aggregation(graph, start_node=None, size=-1, metropolized=False) -> List[int]:
    """
    RW, MHRWでサンプリングしたノード列について、クラスタ係数を100回計算し、
    その平均と分散を返す

    :param graph: グラフ
    :param start_node: 先頭ノード
    :param size: サイズ
    :param metropolized: metropolis hasting random walk フラグ
    :return: {average: 平均, var: 分散}
    """
    if start_node is None:
        start_node = random.choice(graph.nodes())

    cluster_coefficient_average_result = []
    for i in range(1, 100):
        cluster_coefficient_average_result.append(random_walk_sampling_cca(graph, start_node, size, metropolized))

    data = np.array(cluster_coefficient_average_result)
    average = np.average(data)
    var = np.var(data)
    return {"average": average, "var": var}


def degree_distribution(graph):
    """
    次数分布

    :param graph: nx.Graph
    :return: indegree_distribution, outdegree_distribution
    """
    M = nx.to_scipy_sparse_matrix(graph)

    indegrees = M.sum(0).A[0]
    outdegrees = M.sum(1).T.A[0]
    # ノードに入ってくる辺数
    indegree_distribution = np.bincount(indegrees)
    # ノードから出ていく辺数
    outdegree_distribution = np.bincount(outdegrees)
    return indegree_distribution, outdegree_distribution

