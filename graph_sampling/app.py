# coding=utf-8

import json
import networkx as nx
from networkx.readwrite import json_graph
import util
import flask


def create_json_from_file(file):
    G = nx.read_edgelist('../data/input/' + file + '.txt')
    edges = list(util.random_walk(graph=G, size=1000, metropolized=True))
    G1 = nx.Graph()
    G1.add_path(edges)
    for n in G1:
        G1.node[n]['name'] = n
    d = json_graph.node_link_data(G1)
    json.dump(d, open('./static/' + file + '.json', 'w'))
    print('Wrote node-link JSON data to static/' + file + '.json')


app = flask.Flask(__name__)


@app.route('/')
def root():
    return app.send_static_file('static/index.html')


@app.route('/view/amazon')
def view_amazon():
    return app.send_static_file('static/com-amazon.ungraph.html')


@app.route('/view/twitter')
def view_twitter():
    return app.send_static_file('static/twitter_combined.html')


@app.route('/api/twitter')
def twitter():
    create_json_from_file("twitter_combined")
    # return app.send_static_file('visualize/twitter_combined.html')


@app.route('/api/amazon')
def amazon():
    create_json_from_file("com-amazon.ungraph")
    # return app.send_static_file('visualize/com-amazon.ungraph.html')


@app.route('/api/youtube')
def youtube():
    create_json_from_file('com-youtube.ungraph')


if __name__ == '__main__':
    print('\nGo to http://localhost:8010 to see the example\n')
    print('\nStatic html page: http://localhost:8010')
    app.run(port=8010)