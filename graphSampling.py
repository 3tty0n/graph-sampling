# coding=utf-8
import itertools

import networkx as nx
import matplotlib.pyplot as plt

class GraphSampling:

    def __init__(self, G):
        self.G = G

    # 完全グラフを計算する
    def complete_graph(self, n):
        G = nx.Graph()
        if n > 1:
            if G.is_directed():
                edges = itertools.permutations(range(n), 2)
            else:
                edges = itertools.combinations(range(n), 2)
            G.add_edges_from(edges)
            print G.edges()
        return G

    # 完全グラフを表示する
    def complete_graph_show(self, n):
        G = self.complete_graph(n)
        pos = nx.circular_layout(G)
        nx.draw_networkx(G, pos)
        plt.show()

    # あるノードvのクラスタ係数を求める
    def cluster_coefficient_node(self, v):
        return nx.clustering(self.G, v)

    # グラフGの平均クラスタ係数を求める
    def cluster_coefficient_average(self):
        return nx.average_clustering(self.G)

    # グラフGの平均次数を求める
    def average_degree(self):
        values = self.G.degree().values()
        return sum(values) / len(values)

    # 次数分布のグラフを表示する
    def degree_distribution_show(self):
        degree_sequence=sorted(nx.degree(self.G).values(), reverse=True)

        plt.loglog(degree_sequence,'b-',marker='o')
        plt.title("Degree rank plot")
        plt.ylabel("degree")
        plt.xlabel("rank")

        plt.axes([0.45,0.45,0.45,0.45])
        Gcc = sorted(nx.connected_component_subgraphs(self.G), key = len, reverse = True)[0]
        pos = nx.spring_layout(Gcc)
        plt.axis('off')
        nx.draw_networkx_nodes(Gcc, pos, node_size=20)
        nx.draw_networkx_edges(Gcc, pos, alpha=0.4)

        plt.savefig("degree_histogram.png")
        plt.show()

    # グラフGを幅優先探索でサンプリングしそのサンプリングノード列を返す
    def breadth_first_search_nodes(self, n):
        edges = list(nx.bfs_edges(self.G, n, True))
        # 最短経路を出力する
        return self.__search_nodes(edges, n)

    def __search_nodes(self, edges, n):
        last_edge = edges[-1]
        next_node = last_edge[0]
        result = list()
        result.append(last_edge[-1])
        result.append(next_node)
        while not next_node == n:
            last_edge = [t for t in edges if t[-1] == next_node][0]
            next_node = last_edge[0]
            result.append(next_node)
        result.reverse()
        return result


# BA10000 のデータを読み込んでグラフを表示する
def ba10000_show(self):
    G = nx.read_edgelist("data/input/BA10000.txt", nodetype=int)
    pos = {}
    nx.draw(G, pos)
    plt.savefig("data/output/test_graph.png")
    plt.show()


def main():
    # グラフの作成
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (2, 4), (3, 4)])
    g = GraphSampling(G)
    # 隣接するノードを出力
    print G.neighbors(1)
    # ノード全体を出力
    print G.nodes()
    # エッジの数を出力
    print G.number_of_edges()
    # 三角形の数を出力
    print nx.triangles(G)
    # Gをクラスタリングする
    print nx.clustering(G, 1)
    # 指定したノードのクラスタ係数を出力する
    print g.cluster_coefficient_node(3)
    # 平均次数を出力する
    print g.average_degree()
    # 平均クラスタ係数を出力する
    print g.cluster_coefficient_average()
    # 幅優先探索してサンプリングしたノード列を返す
    print g.breadth_first_search_nodes(1)

    # 次数分布の対数グラフを表示する
    # G = nx.gnp_random_graph(100,0.02)
    # g = ShudoGraph(G)
    # g.degree_distribution_show()


def bfs_sampling():
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (4, 7), (4, 8), (5, 9), (5, 10), (7, 11), (7, 12)])
    g = GraphSampling(G)
    print g.breadth_first_search_nodes(1)

    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (2, 4), (3, 4)])
    g = GraphSampling(G)
    print g.breadth_first_search_nodes(1)

if __name__ == '__main__':
    print "bfs sampling\n"
    bfs_sampling()
    print "\n"
    print "main\n"
    main()
