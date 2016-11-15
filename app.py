# coding=utf-8

import json

import flask
import networkx as nx
from networkx.readwrite import json_graph

import util


def create_json_from_file(file):
    G = nx.read_edgelist('../data/input/' + file + '.txt')
    edges = list(util.random_walk(graph=G, size=2000, metropolized=False))
    G1 = nx.Graph()
    G1.add_path(edges)
    for n in G1:
        G1.node[n]['name'] = n
    d = json_graph.node_link_data(G1)
    json.dump(d, open('./static/' + file + '.json', 'w'))
    print('Wrote node-link JSON data to static/' + file + '.json')


graphs = list()
graphs.append({"name": "twitter_combined",
               "url": "/static/twitter_combined.html",
               "generateUrl": "/api/twitter",})
graphs.append({"name": "com-amazon.ungraph",
               "url": "/static/com-amazon.ungraph.html",
               "generateUrl": "api/amazon"})


app = flask.Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def index():
    return flask.render_template('index.html',
                                 title="Forced-layout Visualization",
                                 subtitle="built with flask, NetworkX and D3.js.",
                                 github='https://github.com/3tty0n/graph_sampling',
                                 graphs=graphs)


@app.route('/api/twitter')
def twitter():
    create_json_from_file('twitter_combined')
    return flask.redirect(flask.url_for('index'))


@app.route('/api/amazon')
def amazon():
    create_json_from_file("com-amazon.ungraph")
    return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
    print('\nGo to http://localhost:5000 to see the example\n')
    app.run()