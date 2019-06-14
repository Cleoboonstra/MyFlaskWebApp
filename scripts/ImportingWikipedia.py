import pandas as pd  # 0.24.2
import networkx as nx  # 2.2
import holoviews as hv  # 1.12.1
import holoviews.operation.datashader as hd

hd.shade.cmap = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#999999']
hv.extension('bokeh')

""" Import CSVs """
node_df = pd.read_csv(
    '../databases/wikispeedia/articles.tsv',
    delimiter='\t')  # 4603 articles

""" Parameters """
N = len(node_df.index)
figtype = 'spring'
B_edge_select = False  # select edge boolean (vs. node select)
BB = False  # bundle edges boolean
BS = False  # datashade boolean
# TO DO : integrate categories into nodes
# categories_df = pd.read_csv(
#     '../databases/wikispeedia/categories.tsv',
#     delimiter='\t')

links_df = pd.read_csv(
    '../databases/wikispeedia/links.tsv',
    delimiter='\t')

# print(node_df.Article_Name-categories_df.Article_Name)
# print(node_df[~node_df.isin(categories_df).all(1)])
# print('\n\n',node_df)
# nodec_df = pd.merge(node_df, categories_df, how='inner', on='Article_Name')

""" Make Networkx Graph"""
nodes = node_df['Article_Name'].tolist()
edges = []
for col in range(0, N-1):
    edges.append([links_df.iat[col, 0], links_df.iat[col, 1]])


def make_network(nodes_list, edges_list, weighted):
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes_list, label=True)
    for edge in edges_list:
        if weighted:
            graph.add_edge(edge[0], edge[1], weight=edge[2], width=edge[2])
        else:
            graph.add_edge(edge[0], edge[1])
    return graph


G = make_network(nodes, edges, False)

""" Make HoloViews Graph """

# TO DO : look into Holomap (SLIDER WOOHOO)
def get_net(layout, bundled, edge_select, shade):
    if layout.lower() == 'circle':
        net = hv.Graph.from_networkx(G, nx.layout.circular_layout).relabel('Circular Layout').opts(
            width=650, height=650, xaxis=None,
            yaxis=None, padding=0.1)
    elif layout.lower() == 'spring':
        net = hv.Graph.from_networkx(G, nx.layout.spring_layout, k=0.8, iterations=5).relabel(
            'Force-Directed Fruchterman-Reingold').opts(width=650, height=650, xaxis=None, yaxis=None, padding=0.1)
    #             , node_size=node_dict[i] for i in node_dict.keys())
    else:
        net = "Error 1: layout type must be: 'circle', 'spring'"
    net.opts(width=650, height=650, xaxis=None, yaxis=None, padding=0.1, edge_color_index='weight', edge_cmap='jet')
    if bundled:
        net = hd.bundle_graph(net)
    if edge_select:
        net.opts(inspection_policy='edges')
    if shade:
        net = hd.datashade(net).opts(plot=dict(height=650, width=650))
    return net


hv_graph = get_net('spring', BB, B_edge_select, BS)


def save_file(name):
    file_name = name + '_' + figtype + '_' + str(N) + '_'
    if BB:
        file_name = file_name + 'bundled' + '_'
    else:
        file_name = file_name + 'notbundled' + '_'
    if B_edge_select:
        file_name = file_name + 'edgeselect' + '_'
    else:
        file_name = file_name + 'nodeselect' + '_'
    if BS:
        file_name = file_name + 'datashaded'
    else:
        file_name = file_name + 'notdatashaded'
    file_name = file_name + '.html'
    hv.save(hv_graph, file_name, backend='bokeh')


save_file('Wikipedia')