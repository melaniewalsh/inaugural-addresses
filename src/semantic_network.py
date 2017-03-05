
# coding: utf-8

# In[1]:

import glob
import networkx as nx
import pandas as pd
from __future__ import print_function
from networkx.algorithms import bipartite
import json
from networkx.readwrite import json_graph
from networkx.algorithms import centrality as cn


# In[2]:

df = pd.read_csv("/Users/mwalsh/DARG/inauguration/all_great_nouns.csv", encoding = "iso-8859-1")


# In[4]:

#projection = df[["president", "date", "word", "count"]].groupby(["president", "word"]).count().reset_index()
projection = df[["president", "date", "word", "count"]]


# In[6]:

projection.columns = ["president", "date", "word", "edge weight"]


# In[8]:

edges = projection


# In[26]:

edges.columns = ['Source','date','Target','edge weight']


# In[27]:

G = nx.from_pandas_dataframe(edges, source='Source', target="Target", edge_attr=["edge weight", "date"])


# In[28]:

G.add_nodes_from(edges['Source'], bipartite=0)


# In[29]:

G.add_nodes_from(edges['Target'], bipartite=1)


# In[30]:

top_nodes = set(n for n,d in G.nodes(data=True) if d['bipartite']==0)
bottom_nodes = set(G) - top_nodes


# In[13]:

nx.write_graphml(G, "/Users/mwalsh/DARG/inauguration/semantic_great_nouns.graphml", encoding="iso-8859-1")


# In[22]:

with open('semantic_great_nouns_experiment.json', 'w') as json_file: 
	json.dump(data, json_file, separators = (',', ':'), sort_keys=True, indent=4, ensure_ascii=False)

