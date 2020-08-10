import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from skbio.stats.composition import ilr
from helper import multiplicativeReplacementOfZeros
from clusteringAnalysis import centers, df
from pyvis.network import Network

nodeSizes = df.apply(sum,axis=0)
nodeSizes= nodeSizes.div(nodeSizes.max())

corrType = "rho"
rhoDf = pd.read_csv("rhoDf.csv",index_col=[0])
phiDf = pd.read_csv("phiDf.csv",index_col=[0])

if corrType == "phi":
    correlationMatrix = phiDf
else : 
  correlationMatrix = rhoDf


colorList = ["blue","red","green","yellow","white"]

def colorChampion(centers,champion,columnList,colorList):
    if type(columnList)!=list:
        columnList=columnList.tolist()
    championIndex= columnList.index(champion)
    valAtEachCenter = [centers[i,championIndex] for i in range(centers.shape[0])]
    return colorList[np.argmax(valAtEachCenter)]
#make network
G = nx.Graph()


G.add_nodes_from(rhoDf.columns.tolist())
colorMap = []
for node in G.nodes():
    colorMap.append(colorChampion(centers,node,rhoDf.columns,colorList))
for index,node1 in enumerate(G.nodes()):
    for node2 in G.nodes():
      if corrType == "rho":
          if node1==node2:# node2 in list(G.nodes)[0:index]:
              continue
          pairCorr= correlationMatrix.loc[node1,node2]
          #essential works like normal correlation coefficient rho in [-1,1] 
          minCorr = correlationMatrix[node1].sort_values()[-6] #number of connections to be made (-1 because of self)
          if pairCorr >= minCorr:
      
              normCorr= (pairCorr-minCorr)/(1-minCorr)
              G.add_edge(node1,node2,weight=normCorr)
  #phi in [0,inf] more proportional the closer to 0
      elif corrType=="phi":
          if node1==node2 or node2 in list(G.nodes)[0:index]:
              continue
          pairCorr= correlationMatrix.loc[node1,node2]  
          minCorr = correlationMatrix[node1].sort_values()[6] #number of connections to be made (-1 because of self)
          if pairCorr <= minCorr:
              
              normCorr= (minCorr - pairCorr)/minCorr
              G.add_edge(node1,node2,weight=normCorr)

pos = nx.spring_layout(G,iterations=30)
edge_widths = [w for (*edge, w) in G.edges.data('weight')]
label_dict= {key:key for key in G.nodes}
edge_labels=nx.draw_networkx_labels(G,pos,edge_labels=label_dict)
nx.draw(G, pos, width=edge_widths,width_labels=True,node_color=colorMap)
plt.show()

g=Network(height="100%",width="100%")
# g.toggle_hide_edges_on_drag(True)
g.barnes_hut()
g.from_nx(G)

maxNodeSize = 200
minNodeSize = 50
maxEdgeWidth = 45
minEdgeWidth=3
for index, node in enumerate(g.nodes):
    node["group"] =  colorChampion(centers,node["id"],rhoDf.columns,colorList)
    title = node["id"]
    node["title"] = f"<h3> {title} </h3>"
    node["size"] = max(min( nodeSizes[node["id"]] * maxNodeSize,maxNodeSize),minNodeSize)
for index , edge in enumerate(g.edges):
    edge["width"] =   max(min(edge["weight"]*maxEdgeWidth,maxEdgeWidth),minEdgeWidth)


g.set_options(options="""  
    var options = {
  "nodes": {
    "borderWidth": 2,
    "font": {
      "size": 97
    },
    "shapeProperties": {
      "borderRadius": 5
    }
  },
  "edges": {
    "color": {
      "inherit": true
    },
    "smooth": false
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -80000,
      "springLength": 250,
      "springConstant": 0.001
    },
    "minVelocity": 0.75
  }
}
      """)
# g.show_buttons(filter_=True)
g.show("network.html")


print("done")