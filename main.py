# coding=utf-8

from networkx.readwrite import json_graph
import util
import networkx as nx
import matplotlib.pyplot as plt
import random_walk_proposal as rp


def ba10000_plot():
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
    """
    twitter のグラフを用いてサンプリングする
    :return:
    """
    G = nx.read_edgelist("data/input/twitter_combined.txt", nodetype=int)
    print(util.cluster_coefficient_average(G))
    print(util.random_walk_cca(graph=G, size=100000, metropolized=True))
    print(util.random_walk_aggregation(graph=G, size=10000, metropolized=True))


def youtube_sampling():
    """
    youtube のグラフを用いてサンプリングする
    :return:
    """
    G = nx.read_edgelist("data/input/com-youtube.ungraph.txt", nodetype=int)
    print(util.random_walk_cca(graph=G, size=10000))
    print(util.random_walk_aggregation(graph=G, size=10000, metropolized=False))


def youtube_sampling_plot(size):
    """
    youtube のグラフをサンプリングし、それを画像として出力する
    :param size:
    :return:
    """
    G = nx.read_edgelist("data/input/com-youtube.ungraph.txt", nodetype=int)
    nodes = list(util.random_walk(graph=G, size=size))
    graph = nx.Graph()
    graph.add_path(nodes)
    nx.draw_random(G=graph)
    plt.savefig("data/output/com-youtube.ungraph.rw." + str(size) + ".png")
    plt.show()


def amazon_sampling():
    """
    amazon のグラフをサンプリングする
    :return:
    """
    G = nx.read_edgelist("data/input/com-amazon.ungraph.txt")
    graph = nx.Graph()
    nodes = util.random_walk(graph=G, size=10000)
    graph.add_path(nodes)
    json_graph.node_link_data(graph)
    plt.savefig("data/output/com-amazon.ungraph.rw.png")
    plt.show()


def sampling():
    """
    単純なグラフをサンプリングする
    :return:
    """
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (4, 7), (4, 8), (5, 9), (5, 10), (7, 11), (7, 12)])
    print(util.cluster_coefficient_node(G, 2))
    print(util.average_degree(G))
    print(list(util.random_walk(graph=G, size=10)))


def degree_distribution_plot():
    """ Plot Distribution """
    G = nx.read_edgelist("data/input/com-amazon.ungraph.txt", nodetype=int, create_using=nx.DiGraph())
    indegree, outdegree = util.degree_distribution(G)

    plt.plot(range(len(indegree)),indegree,'bo')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Freq')
    plt.xlabel('Degree')
    plt.savefig('data/output/com-amazon.ungraph.png')
    plt.show()


def level1():
    print('\n---------- LEVEL 1 ---------\n')
    # 次数10の完全グラフをプロットする
    util.complete_graph_show(10)
    # グラフGのあるノードvのクラスタ係数をreturnする
    G = util.complete_graph(10)
    v = 1
    print('cluster coefficient of {0} is {1}'.format(v, util.cluster_coefficient_node(G, v)))


def level2():
    print('\n---------- LEVEL2 ----------\n')
    # グラフGの対数グラフをプロットする
    degree_distribution_plot()
    # グラフGの平均クラスタ係数をreturnする
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (4, 7), (4, 8), (5, 9), (5, 10), (7, 11), (7, 12)])
    print('average cluster coefficient of G is {0}'.format(util.cluster_coefficient_average(G)))


def level3():
    print('\n---------- LEVEL3 ----------\n')
    # グラフGを幅優先探索でサンプリングを行い、そのサンプリングノード列をreturnする
    G = util.complete_graph(10)
    print('bfs sampling nodes: {0}'.format(util.bfs(G, 1, 4)))
    # グラフGをRWでサンプリングを行い、そのサンプリングノード列をreturnする
    G = nx.read_edgelist("data/input/com-amazon.ungraph.txt")
    print('random walk sampling of amazon graph: {0}'
          .format(list(util.random_walk(graph=G, size=3000, metropolized=False))))
    # グラフGをMHRWでサンプリングを行い、そのサンプリングノード列をreturnする
    print('Metropolis hasting random walk of amazon graph: {0}'
          .format(list(util.random_walk(graph=G, size=3000, metropolized=True))))


def level4():
    print('\n---------- LEVEL4 ----------\n')
    G = nx.read_edgelist("data/input/com-amazon.ungraph.txt")
    # グラフGをRWでサンプリングを行い、そのグラフのクラスタ係数を推定値をreturnする
    print('Cluster coefficient of sampled graph' +
          'by random walk (one time): {0}'.format(util.random_walk_cca(graph=G, size=5000)))
    # グラフGをMHRWでサンプリングを行い、そのグラフのクラスタ係数を推定値をreturnする
    print('Cluster coefficient of sampled graph' +
          'by metropolis hasting random walk (one time): {0}'
          .format(util.random_walk_cca(graph=G, size=5000, metropolized=True)))
    # 上記の関数を100回適応し、平均、分散、NMSEを出力する
    print('Random Walk: {0}'
          .format(util.random_walk_aggregation(G, size=5000, tv=0.3967)))
    print('Metropolis hasting random walk: {0}'
          .format(util.random_walk_aggregation(G, size=5000, metropolized=True, tv=0.3967)))


if __name__ == "__main__":
    G = nx.read_edgelist('data/input/com-amazon.ungraph.txt')
    # print(util.random_walk_aggregation(graph=G, size=2000, pg=False, tv=0.3967))
    print(util.random_walk_aggregation(graph=G, size=2000, metropolized=False, tv=0.3967))
