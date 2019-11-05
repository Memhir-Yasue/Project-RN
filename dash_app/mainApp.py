import dash
import dash_cytoscape as cyto
import dash_html_components as html
import networkx as nx
import json
from user_hub.user import User
from user_hub import time_box
cyto.load_extra_layouts()

def run_User(user: str):
    redditor = User(user)
    redditor.validate_user()
    redditor.get_visited_pages()
    visited, t_stamp, t_stamp_subreddit = redditor.return_user_attributes()
    edges = time_box.process_to_edges(t_stamp_subreddit)
    return visited, t_stamp, edges


def run_networkX(visited, time_stamp, edges):
    nodes = list(visited.keys()) + list(time_stamp.keys())
    G = nx.Graph()
    G.add_nodes_from(nodes)
    clean_edge = []
    for pair in edges:
        if pair not in clean_edge:
            clean_edge.append(pair)
    G.add_edges_from(clean_edge)
    return G, clean_edge


def convert_to_cytoscape(G):
    nodes = nx.readwrite.json_graph.cytoscape_data(G).get('elements').get('nodes')
    locations = nx.nx_agraph.graphviz_layout(G)
    locations = json.dumps(locations)  # convert all keys to string
    locations = json.loads(locations)  # convert stringized dict back to dict
    list_pair = []
    for i in range(len(nodes)):
        node_name = nodes[i]['data']['id']
        location = locations.get(node_name)
        node = nodes[i]
        formatted_node_info = {'data': {'id': node_name, 'label': node_name},
                               'position': {'x': location[0], 'y': location[1]}}
        list_pair.append(formatted_node_info)
    return list_pair

def clean_up(list_pair: list):
    dash_input = []
    for elements in list_pair:
        for i in range(2):
            dash_input.append(elements[i])
    return dash_input

def append_edge_connection(dash_input,edges: dict):
    for i in range(len(edges)):
        source = str(edges[i][0])
        target = str(edges[i][1])
        dash_input.append({'data': {'source': source,
                                    'target': target}})
    return dash_input


visited, t_stamp, edges = run_User('coordinatedflight')
G, edges = run_networkX(visited, t_stamp, edges)
dash_input = convert_to_cytoscape(G)
dash_input = append_edge_connection(dash_input,edges)

app = dash.Dash(__name__)
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'spread'},
        style={'width': '100%', 'height': '1000px'},
        elements=dash_input
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)