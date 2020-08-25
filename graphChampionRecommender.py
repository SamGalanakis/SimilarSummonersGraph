import networkx as nx
import argparse
from Levenshtein import distance
import numpy as np
from pyvis.network import Network
import pickle




G = nx.read_gpickle("network.gpickle")
with open("data//pyvisNetwork.pickle", "rb") as f:
     g=pickle.load(f)



def recommendChampion(champList,network):

    weightedDistDict = dict(nx.all_pairs_dijkstra_path_length(network,weight ="cost"))

    avgDistDict = {key:0 for key in network.nodes}
    #Get sum average distance to all champions for all input champions 
    for champ in champList:
        for key,value in weightedDistDict[champ].items():
            avgDistDict[key]+=value/len(champList)
    # Recommend shortest distance champ that isn't in input set
    for item  in sorted(list(avgDistDict.items()),key = lambda x: x[1])  : 
        if item[0] not in champList:
            return item[0]
    


if __name__ == "__main__":
    


    parser = argparse.ArgumentParser(description='Network based champion recommender')


    parser.add_argument('--champions', type=str, nargs='+',
                        help="Champion names as so : \"Ashe\" \"Master Yi\" \"Zoe\" ")


    args = parser.parse_args()
    championList= getattr(args, "champions")
    
    validChamps = list(G.nodes )

    #Make sure valid champs, suggest close champ match if not
    for champ in championList:
   
        if champ not in G.nodes():
    
            distances = [distance(champ,x) for x in validChamps ]
            print(distances)
            closestChamp = validChamps[np.argmin(distances)]
            errorText = f"{champ} not a valid champion name, closest champ is {closestChamp}"
            raise Exception(errorText)
    

    #get champions in input and on shortest paths to recommended
    recommendation = recommendChampion(championList,G)
    relevantNodes = set()
    for champ in championList:
       relevantNodes.update(set(nx.shortest_path(G,champ,recommendation))) 



    
    #filter out irrelevant nodes

    g.nodes = [x for x in g.nodes if x["id"] in relevantNodes]
  
    g.heading = f"Recommended champ: {recommendation}, showing shortest paths from inputted champions"
    g.bgcolor = "#99ccff"
    g.show("networkRecommendationSubset.html")
    
    print(f"Recommended champ: {recommendation}")
