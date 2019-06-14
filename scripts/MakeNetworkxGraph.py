# Asaf
import scripts.ImportGeneral
import networkx as nx
import math
import operator

""" ########################## """
""" Make node and edge weights """
""" ########################## """


def make_node_degrees(nodes_list, edges_list):
    # dictionary where key is node name, value is count of edges
    node_degrees = {node: 0 for node in nodes_list}

    # make node size based on edge count
    for edge in edges_list:
        if edge[0] in node_degrees.keys(): node_degrees[edge[0]] = node_degrees[edge[0]] + 1

    return node_degrees


def really_safe_normalise_in_place(d):
    factor = 1.0 / math.fsum(d.values())
    min_size = 10
    for k in d:
        # + 1 fixes minimum sizes
        d[k] = d[k] * factor + min_size
    key_for_max = max(d.items(), key=operator.itemgetter(1))[0]
    diff = 1.0 - math.fsum(d.values())
    # print "discrepancy = " + str(diff)
    d[key_for_max] += diff
    return d


def min_max_normalise(d):
    # Min-Max Feature scaling, form:
    # z_i = (x_i - Xmin)/(Xmax - Xmin) OR
    # z_i = a + (x_i - Xmin)*(b-a) /(Xmax - Xmin)

    # Get max and min values
    key_for_max = max(d.items(), key=operator.itemgetter(1))[0]
    Xmax = d[key_for_max]

    key_for_min = min(d.items(), key=operator.itemgetter(1))[0]
    Xmin = d[key_for_min]

    # Make normalized array to represent sizes
    z = d.copy()
    min_size = 10
    max_size = 100
    for key in z:
        z[key] = min_size + ((d[key] - Xmin) * (max_size - min_size)) \
                 / (Xmax - Xmin)
    return z


def make_node_sizes(nodes_list, edges_list):
    dic = make_node_degrees(nodes_list, edges_list)
    for k in dic:
        dic[k] = dic[k]
    new_dic = min_max_normalise(dic)
    for k in new_dic:
        new_dic[k] = int(new_dic[k])
    return new_dic


""" Edge weights module """


def make_edge_weights(nodes_list, edges_list):
    dic = make_node_degrees(nodes_list, edges_list)
    edge_weights = []
    for edge in edges_list:
        try:
            edge_weights.append([edge[0], edge[1], dic[edge[0]] + dic[edge[1]]])
        except:
            edge_weights.append([edge[0], edge[1], dic[edge[0]]])

    return edge_weights


def make_normalized_edge_weights(nodes_list, edges_list):
    # Min-Max Feature scaling, form:
    # z_i = (x_i - Xmin)/(Xmax - Xmin) OR
    # z_i = a + (x_i - Xmin)*(b-a) /(Xmax - Xmin)

    edge_weights = make_edge_weights(nodes_list, edges_list)

    # Get max and min values
    Xmax = max(edge[2] for edge in edge_weights)
    Xmin = min(edge[2] for edge in edge_weights)

    # Make normalized array to represent sizes
    normalized_weights = edge_weights.copy()
    min_size = 1
    max_size = 30
    for i in range(0, len(normalized_weights) - 1):
        normalized_weights[i][2] = min_size + ((normalized_weights[i][2] - Xmin) * (max_size - min_size)) \
                                / (Xmax - Xmin)

    return normalized_weights


""" ############ """
""" Make Networkx """
""" ############ """


# Make networkx graph
def make_network(nodes_list, edges_list, weighted, cat_nodes_list=None, cat_links_list=None, node_type=None,
                 cat_type=None):
    graph = nx.DiGraph()

    # Make node dimensions
    node_degrees = make_node_degrees(nodes_list, edges_list)
    node_sizes = make_node_sizes(nodes_list, edges_list)

    # Make edges
    if weighted == False:
        weighted_edges = make_normalized_edge_weights(nodes_list, edges_list)
        edges_list = weighted_edges

    # Add non category nodes and edges to graph
    if node_type is None:
        for node in nodes_list:
            graph.add_node(node, label=True, degree=node_degrees[node],
                           size=node_sizes[node], node_type=node)

        for edge in edges_list:
            graph.add_edge(edge[0], edge[1], weight=edge[2])

    else:
        for node in nodes_list:
            graph.add_node(node, label=True, degree=node_degrees[node],
                           size=node_sizes[node], node_type=node_type)
            for edge in edges_list:
                graph.add_edge(edge[0], edge[1], weight=edge[2], edge_type=node_type)

    # Make category nodes, edges, add to graph
    if cat_nodes_list is not None and cat_links_list is not None:
        cat_degrees = make_node_degrees(cat_nodes_list, cat_links_list)
        cat_sizes = make_node_sizes(cat_nodes_list, cat_links_list)

        # Add nodes to graph
        for node in cat_nodes_list:
            graph.add_node(node, label=True, degree=cat_degrees[node],
                           size=cat_sizes[node], node_type=cat_type)

        # Add edges to graph
        cat_weighted_edges = make_normalized_edge_weights(cat_nodes_list, cat_links_list)
        cat_edges_list = cat_weighted_edges
        for edge in cat_edges_list:
            graph.add_edge(edge[0], edge[1], weight=edge[2], edge_type=cat_type)

    return graph


""" ################################### """
""" Make CATEGORY node and edge weights """
""" ################################### """
# TO DO: fix this
# def make_cat_network(nodes, links, categoriesdf, cat_cols):
#     G = make_network(nodes, links)

#     cat_list = categoriesdf[cat_cols[1]].tolist()
#     ucat_list = list(set(cat_list))

#     # make category edges
#     cat_links = []
#     for col in range(0, len(cat_list) - 1):
#         cat_links.append([categoriesdf.iat[col, 0], categoriesdf.iat[col, 1]])

#     # add category edge weights
#     """ DO THIS """
#     cat_links = make_edge_weights(ucat_list, cat_links)

#     # category dimensions
#     cat_degrees = make_node_degrees(ucat_list, cat_links)
#     cat_sizes = make_node_sizes(ucat_list, cat_links)

#     # add cat nodes to graph
#     for cat in ucat_list:
#         G.add_node(cat, label=True, degree=cat_degrees[cat], size=cat_sizes[cat], node_color='#df3a10')

#     # add cat edges to graph
#     for link in cat_links:
#         G.add_edge(link[0], link[1], weight=link[2], edge_color='#df3a10')
#     return graph


# TO DO: remove, not holoviews
# plt.figure(figsize=(50,50))

""" ####### """
""" DO THIS """
""" ####### """


# TO DO: return graph G

# TO DO: add functionality
def __makegraph__(sep_type, nodes_df_link, links_df_link=None, cats_df_link=None, weighted=False):
    if cats_df_link is None:
        nodes_list, edges_list, node_type = \
            scripts.ImportGeneral.importcsv(sep_type, nodes_df_link, links_df_link, cats_df_link)
        cat_nodes_list, cat_links_list, cat_type = None, None, None
    else:
        nodes_list, edges_list, cat_nodes_list, cat_links_list, node_type, cat_type = \
            scripts.ImportGeneral.importcsv(sep_type, nodes_df_link, links_df_link, cats_df_link)

    G = make_network(nodes_list=nodes_list, edges_list=edges_list,
                     cat_nodes_list=cat_nodes_list, cat_links_list=cat_links_list,
                     weighted=weighted, node_type=node_type, cat_type=cat_type)
    # TO DO: 'serialize' G object (represent it as binary file and save it as cookie)
    return G

# TO DO: remove, not holoviews
# nx.draw_spring(G, node_size=[v*100 for v in degrees.values()],with_labels=True, edge_color='#ffff00')
# plt.show()
# END TO DO
