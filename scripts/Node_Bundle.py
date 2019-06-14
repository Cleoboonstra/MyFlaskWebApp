# Asaf
import scripts.MakeNetworkxGraph
import holoviews as hv
import networkx as nx
from holoviews.operation.datashader import datashade, bundle_graph
from app import *


# INPUT UPLOADED FILE
def node_bundle_tab(filename):
    G = scripts.MakeNetworkxGraph.__makegraph__(sep_type='semicolon', nodes_df_link=filename)
    """ Make HV network """
    hv_graph = hv.Graph.from_networkx(G, nx.spring_layout, k=1).relabel('Force-Directed Spring')

    hv_graph.opts(width=650, height=650, xaxis=None, yaxis=None,
                  padding=0.1, node_size=hv.dim('size'),
                  node_color=hv.dim('node_type'), cmap='YlOrBr',
                  edge_color=hv.dim('weight'), edge_cmap='YlGnBu', edge_line_width=hv.dim('weight'))

    bundle_graph_plot = bundle_graph(hv_graph)

    """ END HERE """

    # Output files to Flask
    renderer = hv.renderer('bokeh')
    # plot = renderer.get_plot(hv_graph, show=True).state
    bundle_plot = renderer.get_plot(bundle_graph_plot, show=True).state
    return bundle_plot

