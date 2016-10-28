# coding=utf-8
import itertools

import networkx as nx
import matplotlib.pyplot as plt
import random


# 完全グラフを計算する
def complete_graph(n):
    G = nx.Graph()
    if n > 1:
        if G.is_directed():
            edges = itertools.permutations(range(n), 2)
        else:
            edges = itertools.combinations(range(n), 2)
        G.add_edges_from(edges)
    return G


# 完全グラフを表示する
def complete_graph_show(graph, n):
    G = graph.complete_graph(n)
    pos = nx.circular_layout(G)
    nx.draw_networkx(G, pos)
    plt.show()


# あるノードvのクラスタ係数を求める
def cluster_coefficient_node(graph, v):
    return nx.clustering(graph, v)


# グラフGの平均クラスタ係数を求める
def cluster_coefficient_average(graph):
    return nx.average_clustering(graph)


# グラフGの平均次数を求める
def average_degree(graph):
    values = graph.degree().values()
    return sum(values) / len(values)


# 次数分布のグラフを表示する
def degree_distribution_show(graph):
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


# 幅優先探索をする
def bfs(graph, start, end):
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


def random_walk_sampling(graph, start_node=None, size=-1, metropolized=False):

    if start_node is None:
        start_node = random.choice(graph.nodes())

    nodes = list(random_walk(graph=graph, start_node=start_node, size=size, metropolized=metropolized))

    graph = nx.Graph()
    graph.add_path(nodes=nodes)

    return cluster_coefficient_average(graph)


# BA10000 のデータを読み込んでグラフを表示する
def ba10000_show():
    G = nx.read_edgelist("data/input/BA10000.txt", nodetype=int)
    pos = {}
    nx.draw(G, pos)
    plt.savefig("data/output/test_graph.png")
    plt.show()


def sampling():
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (4, 7), (4, 8), (5, 9), (5, 10), (7, 11), (7, 12)])
    # print nx.bfs_successors(G, 1)
    # print list(random_walk(graph=G, start_node=1, size=10, metropolized=True))

    G2 = nx.read_edgelist("data/input/BA10000.txt", nodetype=int)
    print(random_walk_sampling(graph=G2, size=100000, metropolized=True))


if __name__ == '__main__':
    sampling()
