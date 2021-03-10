import networkx as nx
import matplotlib.pyplot as plt
import netwulf as nw
from netwulf import visualize
import os
import csv
import pandas as pd

def createnxgraph(filename, seperator):
    with open(filename) as infile:
        csv_reader = csv.reader(infile,delimiter=seperator)
        G = nx.Graph(csv_reader)
    return G

def get_network_statistics(g):
    num_connected_components = nx.number_connected_components(g)
    num_nodes = nx.number_of_nodes(g)
    num_edges = nx.number_of_edges(g)
    density = nx.density(g)
    avg_clustering_coef = nx.average_clustering(g)
    degree_values = dict(g.degree()).values()
    avg_degree = sum(degree_values) / float(num_nodes)
    transitivity = nx.transitivity(g)
    diameter=15

    network_statistics = {
        'num_connected_components':num_connected_components,
        'num_nodes':num_nodes,
        'num_edges':num_edges,
        'density':density,
        'diameter':diameter,
        'avg_clustering_coef':avg_clustering_coef,
        'avg_degree':avg_degree,
        'transitivity':transitivity
    }

    df = pd.DataFrame(
    [
        (
            "No. of connected components",
            network_statistics.get('num_connected_components'),
        ),
        (
            "No. of Nodes",
            network_statistics.get('num_nodes'),
        ),
        (
            "No. of Edges",
            network_statistics.get('num_edges'),
        ),
        (
            "Density",
            network_statistics.get('density'),
        ),
        (
            "Diameter",
            network_statistics.get('diameter'),
        ),
        (
            "Avg. clustering coeff.",
            network_statistics.get('avg_clustering_coef'),
        ),
        (
            "Avg. Degree",
            network_statistics.get('avg_degree'),
        ),
        (
            "Transitivity",
            network_statistics.get('transitivity'),
        ),
    ],
    columns=("Property", "Value"),
    ).set_index("Property")

    return df
