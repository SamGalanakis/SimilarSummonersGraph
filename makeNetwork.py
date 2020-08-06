import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


df = pd.read_csv("withYone.csv")
df=df.drop("summoner",axis=1)
df = df.div(df.sum(axis=1), axis=0) # normalize each players stats by sum of row, so get percentage mastery
corr = df.corr()
# corr=corr[corr.loc["Yasuo"]>0.95]
# plt.scatter(corr.index,corr["Yasuo"])
# plt.xticks(rotation=45)
# plt.show()



#make network
G = nx.Graph()

G.add_nodes_from(corr.columns.tolist())

for index,node1 in enumerate(G.nodes()):
    for node2 in G.nodes():
        if node1==node2 or node2 in list(G.nodes)[0:index]:
            continue
        pairCorr= corr.loc[node1,node2]
        minCorr = 0.9
        if pairCorr > minCorr:
            normCorr = pairCorr
            # normCorr= (pairCorr - minCorr)/(1-minCorr)
            G.add_edge(node1,node2,width=normCorr)

pos = nx.spring_layout(G,iterations=30)
edge_widths = [w for (*edge, w) in G.edges.data('width')]
label_dict= {key:key for key in G.nodes}
edge_labels=nx.draw_networkx_labels(G,pos,edge_labels=label_dict)
nx.draw(G, pos, width=edge_widths,width_labels=True)
plt.show()




print("done")