# Asaf
import pandas as pd  # 0.24.2
import networkx as nx  # 2.2
from matplotlib import pyplot as plt
from collections import Counter
import holoviews as hv

hv.extension('bokeh', 'matplotlib')

# Turn dataframes to lists


def get_cols(df):
    return df.columns.tolist()


def node_list(node_df):
    columns = get_cols(node_df)
    nodes = node_df[columns[0]].tolist()
    return nodes


def link_list(node_df, links_df):
    N = len(node_list(node_df))
    links = []

    for col in range(0, N - 1):
        links.append([links_df.iat[col, 0], links_df.iat[col, 1]])

    return links

""" ########### """
""" Import CSVs """
""" ########### """


# TO DO: single CSV Gephi input
def importsingle(node_csv, separation_type):
    # Make nodes
    if separation_type == "semicolon":
        df = pd.read_csv(
            node_csv,
            delimiter=';')  # 4603 articles
    elif separation_type == "tab":
        df = pd.read_csv(
            node_csv,
            delimiter='\t')  # 4603 articles
    elif separation_type == 'comma':
        df = pd.read_csv(
            node_csv,
            delimiter=',')  # 4603 articles
    else:
        df = 'Broken'
        print("Please choose 'comma', 'semicolon' or 'tab'.")

    print(df)
    # Make edges
    edges_list = []
    nodes_list = df.columns.tolist()
    N = len(df.columns)

    for row in range(0, N-1):
        for col in range(0, N-1):
            cell = df.iat[row,col]
            if int(cell) > 0:
                edges_list.append([nodes_list[row], nodes_list[col], df.iat[row, col]])

    # output as lists
    return nodes_list, edges_list


""" #################### """
""" Import multiple CSVs """
""" #################### """

# import nodes, links, categories, by separation type
def importcsv(separation_type, node_csv, link_csv=None, categories_csv=None):
    if link_csv is None:
        nodes_list, links_list = importsingle(separation_type=separation_type, node_csv=node_csv)
        return nodes_list, links_list, None
    else:
        if separation_type == "semicolon":
            nodes = pd.read_csv(node_csv, delimiter=';')  # 4603 articles
            if link_csv is not None: links = pd.read_csv(link_csv, delimiter=';')
            if categories_csv is not None: categories = pd.read_csv(categories_csv, delimiter=';')
        elif separation_type == "tab":
            nodes = pd.read_csv(node_csv, delimiter='\t')  # 4603 articles
            if link_csv is not None: links = pd.read_csv(link_csv, delimiter='\t')
            if categories_csv is not None: categories = pd.read_csv(categories_csv, delimiter='\t')
        elif separation_type == 'comma':
            nodes = pd.read_csv(node_csv, delimiter=',')  # 4603 articles
            if link_csv is not None: links = pd.read_csv(link_csv, delimiter=',')
            if categories_csv is not None: categories = pd.read_csv(categories_csv, delimiter=',')
        else:
            nodes = 'Broken'
            if link_csv is not None: links = 'Broken'
            if categories_csv is not None: categories = 'Broken'
            print("Please choose 'comma', 'semicolon' or 'tab'.")

        nodes_list = node_list(nodes)
        links_list = link_list(nodes, links)

        node_cols = get_cols(nodes)
        node_type = node_cols[0]

    if categories_csv is None:
        return nodes_list, links_list, node_type

    else:
        # Make category nodes
        cat_cols = get_cols(categories)
        cat_type = cat_cols[1]

        cat_nodes_list = categories[cat_cols[1]].tolist()  # ASSUMPTION: category csv form: node, category
        cat_nodes_list = list(set(cat_nodes_list))

        # Make category edges (category -> node)
        cat_links_list = []
        for col in range(0, len(cat_nodes_list) - 1):
            cat_links_list.append([categories.iat[col, 1], categories.iat[col, 0]])

        return nodes_list, links_list, cat_nodes_list, cat_links_list, node_type, cat_type
