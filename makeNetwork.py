import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from skbio.stats.composition import ilr
from helper import multiplicativeReplacementOfZeros
from clusteringAnalysis import centers

print(centers)

df = pd.read_csv("rhoDf.csv",index_col=[0])

colorList = ["blue","red","green","yellow","white"]

def colorChampion(centers,champion,columnList,colorList):
    if type(columnList)!=list:
        columnList=columnList.tolist()
    championIndex= columnList.index(champion)
    valAtEachCenter = [centers[i,championIndex] for i in range(centers.shape[0])]
    return colorList[np.argmax(valAtEachCenter)]
#make network
G = nx.Graph()


G.add_nodes_from(df.columns.tolist())
colorMap = []
for node in G.nodes():
    colorMap.append(colorChampion(centers,node,df.columns,colorList))
for index,node1 in enumerate(G.nodes()):
    for node2 in G.nodes():
        if node1==node2 or node2 in list(G.nodes)[0:index]:
            continue
        pairCorr= df.loc[node1,node2]
        minCorr = df[node1].sort_values()[-6]
        if pairCorr > minCorr:
            normCorr = pairCorr
            normCorr= (pairCorr-minCorr)/(1-minCorr)
            G.add_edge(node1,node2,width=normCorr)

pos = nx.spring_layout(G,iterations=30)
edge_widths = [w for (*edge, w) in G.edges.data('width')]
label_dict= {key:key for key in G.nodes}
edge_labels=nx.draw_networkx_labels(G,pos,edge_labels=label_dict)
nx.draw(G, pos, width=edge_widths,width_labels=True,node_color=colorMap)
plt.show()




print("done")