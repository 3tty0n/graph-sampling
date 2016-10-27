# coding=utf-8
import itertools

import networkx as nx
import matplotlib.pyplot as plt

class ShudoGraph:
    def __init__(self, n, graph):
        self.n = n
        self.graph = graph

    @staticmethod
    def show_ba10000():
        G = nx.read_edgelist("data/input/BA10000.txt", nodetype=int)
        pos = {}
        nx.draw(G, pos)
        plt.savefig("data/output/test_graph.png")
        plt.show()

    # 完全グラフを計算する
    def complete_graph(self):
        G = nx.Graph()
        if self.n > 1:
            if G.is_directed():
                edges = itertools.permutations(range(self.n), 2)
            else:
                edges = itertools.combinations(range(self.n), 2)
            G.add_edges_from(edges)
            print G.edges()
        return G

    # 完全グラフを表示する
    def show_complete_graph(self):
        G = self.complete_graph()
        pos = nx.circular_layout(G)
        nx.draw_networkx(G, pos)
        plt.show()

    # あるノードvのクラスタ係数を求める
    def cluster_coefficient_node(self, v):
        return nx.clustering(self.graph, v)

    # グラフGの平均次数を求める
    def average_degree(self):
        values = self.graph.degree().values()
        return sum(values) / len(values)

if __name__ == '__main__':
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (2, 4), (3, 4)])
    g = ShudoGraph(10, G)
    print G.neighbors(1), G.nodes(), G.number_of_edges()
    print nx.triangles(G), nx.clustering(G, 1)
    print g.cluster_coefficient_node(3)
    print g.average_degree()

