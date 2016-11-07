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


graphs = list()
graphs.append({"name": "twitter_combined",
               "url": "/static/twitter_combined.html",
               "generateUrl": "/api/twitter",})
graphs.append({"name": "com-amazon.ungraph",
               "url": "/static/com-amazon.ungraph.html",
               "generateUrl": "api/amazon"})
graphs.append({"name": "com-youtube.ungraph",
               "url": "/static/com-youtube.ungraph.html",
               "generateUrl": "api/youtube"})

app = flask.Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def hello():
    return flask.render_template('index.html',
                                 title="Forced-layout Visualization",
                                 subtitle="built with flask.",
                                 github='https://github.com/3tty0n/graph_sampling',
                                 graphs=graphs)


@app.route('/api/twitter')
def twitter():
    create_json_from_file("twitter_combined")
    return app.send_static_file('/static/twitter_combined.html')


@app.route('/api/amazon')
def amazon():
    create_json_from_file("com-amazon.ungraph")
    return app.send_static_file('/static/com-amazon.ungraph.html')


@app.route('/api/youtube')
def youtube():
    create_json_from_file('com-youtube.ungraph')
    return app.send_static_file('/static/com-youtube.ungraph.html')


if __name__ == '__main__':
    print('\nGo to http://localhost:5000 to see the example\n')
    app.run()