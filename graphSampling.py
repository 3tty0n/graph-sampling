# coding=utf-8

import itertools
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random


def complete_graph(n):
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


def cluster_coefficient_node(graph, v):
    """
    graphのあるノードvのクラスタ係数を求める

    :param graph: グラフ
    :param v: ノード
    :return:
    """
    return nx.clustering(graph, v)


def cluster_coefficient_average(graph):
    """
    graphの平均クラスタ係数を求める
    :param graph: グラフ
    :return: 平均クラスタ係数
    """
    return nx.average_clustering(graph)


def average_degree(graph):
    """
    graphの平均次数を求める
    :param graph: グラフ
    :return: 平均次数
    """
    values = graph.degree().values()
    data = np.array(values)
    return np.average(data)


# 次数分布のグラフを表示する
def degree_distribution_show(graph):
    """
    graphの次数分布のグラフを描画する
    :param graph: グラフ
    :return:
    """
    degree_sequence = sorted(nx.degree(graph).values(), reverse=True)

    plt.loglog(degree_sequence, 'b-', marker='o')
    plt.title("Degree rank plot")
    plt.ylabel("degree")
    plt.xlabel("rank")

    plt.axes([0.45, 0.45, 0.45, 0.45])
    Gcc = sorted(nx.connected_component_subgraphs(graph), key=len, reverse=True)[0]
    pos = nx.spring_layout(Gcc)
    plt.axis('off')
    nx.draw_networkx_nodes(Gcc, pos, node_size=20)
    nx.draw_networkx_edges(Gcc, pos, alpha=0.4)

    plt.savefig("degree_histogram.png")
    plt.show()


def bfs(graph, start, end):
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


# RWでサンプリングしたノード列を返す
def random_walk(graph, start_node=None, size=-1, metropolized=False):
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


# RWでサンプリングしたグラフの平均クラスタ係数を求める
def random_walk_sampling(graph, start_node=None, size=-1, metropolized=False):
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


def random_walk_aggregation(graph, start_node=None, size=-1, metropolized=False):
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
        cluster_coefficient_average_result.append(random_walk_sampling(graph, start_node, size, metropolized))

    data = np.array(cluster_coefficient_average_result)
    average = np.average(data)
    var = np.var(data)
    return {"average": average, "var": var}


def ba10000_show():
    """
    BA10000.txtを読み込んでグラフを表示する
    :return:
    """
    G = nx.read_edgelist("data/input/BA10000.txt", nodetype=int)
    pos = {}
    nx.draw(G, pos)
    plt.savefig("data/output/test_graph.png")
    plt.show()


def twitter_sampling():
    G = nx.read_edgelist("data/input/twitter_combined.txt", nodetype=int)
    print(cluster_coefficient_average(G))
    print(random_walk_sampling(graph=G, size=100000, metropolized=True))
    print(random_walk_aggregation(graph=G, size=10000, metropolized=True))


def youtube_sampling():
    G = nx.read_edgelist("data/input/com-youtube.ungraph.txt", nodetype=int)
    print(random_walk_sampling(graph=G, size=10000))
    print(random_walk_aggregation(graph=G, size=10000, metropolized=False))


def youtube_sampling_show(size):
    G = nx.read_edgelist("data/input/com-youtube.ungraph.txt", nodetype=int)
    nodes = list(random_walk(graph=G, size=size))
    graph = nx.Graph()
    graph.add_path(nodes)
    nx.draw_random(G=graph)
    plt.savefig("data/output/youtube_rw" + str(size) + ".png")
    plt.show()


def sampling():
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (4, 7), (4, 8), (5, 9), (5, 10), (7, 11), (7, 12)])
    print(nx.bfs_successors(G, 1))
    print(list(random_walk(graph=G, start_node=1, size=10, metropolized=True)))


if __name__ == '__main__':
    youtube_sampling_show(1000)
