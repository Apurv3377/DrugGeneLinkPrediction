import pandas as pd
import stellargraph as sg
from stellargraph.data import EdgeSplitter
from sklearn.model_selection import train_test_split
import pickle
from IPython.display import Image, HTML
from math import log
import os
import numpy as np

def CreateGraph(filename, seperator, *args):
    edges = pd.read_csv(filename, sep=seperator)

    drugs = pd.DataFrame(index=pd.unique(edges[args[0]]))
    genes = pd.DataFrame(index=pd.unique(edges[args[1]]))

    graphObj = sg.StellarGraph(
        {"drug": drugs, "gene": genes},
        edges,
        source_column=args[0],
        target_column=args[1],
    )
    return graphObj

# For node2vec graph is splitted into three different subgraphs.
#1. Test Graph (Test graph and Test set) where first is to compute node embeddings and second is set of positive and negative edges for testing classifiers.
#2. Train Graph (Train graph and Train set) where first is to compute node embeddings and second is set of positive and negative edges for training classifiers.
#3. Model selection Set is for selecting the best classifier with different binary operators.

# Randomly sample a fraction p=0.1 of all positive links, and same number of negative links, from graph, and obtain the
# reduced graph graph_test with the sampled links removed:
# Here we are using 'global' method as node2vec also uses same random selection in their link prediction experiment from paper.

def SplitGraphObj(graphObj):
    # Creating splitter object using EdgeSplitter and create test graph and test set.
    # Test graph is a reduced version of original graph obtained by removing links from test set.
    # Here we are samping 0.1 which is ~10% of positive and negative links and creating Test set.

    test_splitobj = EdgeSplitter(graphObj)
    test_graph, edgelist_test, labels_test = test_splitobj.train_test_split(
    p=0.1, method="global")

    # Creating train set and train graph further using reduced test graph
    # train_test_split returns 'reduced graph (positive edges removed)' ,
    #'N*2 dim edgelist for pos and neg edges sampled',
    #'labels '0' and '1' based for neg and pos edge resp'

    train_splitobj = EdgeSplitter(test_graph, graphObj)
    train_graph, edgelist, labels = train_splitobj.train_test_split(
        p=0.1, method="global"
    )

    #Using sklearn train_test_split method to split the edgelist and labels
    #Here we are splitting into 75% and 25% to generate model selection and train set.

    (   edgelist_train,
        edgelist_model_selection,
        labels_train,
        labels_model_selection,
    ) = train_test_split(edgelist, labels, train_size=0.75, test_size=0.25)

    return test_graph, train_graph, edgelist_test, edgelist_train,edgelist_model_selection, labels_test ,labels_train, labels_model_selection
