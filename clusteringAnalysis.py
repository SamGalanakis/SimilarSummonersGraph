import pandas as pd
from skbio.stats.composition import ilr, ilr_inv, clr, _gram_schmidt_basis,clr_inv,closure
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
from helper import multiplicativeReplacementOfZeros
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from collections import Counter
tqdm.pandas()
df=pd.read_csv("mainData.csv")

df=df.drop("summoner",axis=1)
minCPfilter  = 	21600 #mastery 5 
df= df[df.max(axis=1)>minCPfilter] #remove players with all champs below some mastery level
replacement_val = df.values[df.values>0].min() #minimum nonzero mastery points 
df = df.progress_apply(lambda x :multiplicativeReplacementOfZeros(x,inputeVal=replacement_val),axis=1) 
df = df.div(df.sum(axis=1), axis=0) # normalize each players stats by sum of row, so get percentage mastery

clrVals = clr(df.values)


scaler = StandardScaler()
scaled_features = scaler.fit_transform(df)

#Kmeans clustering
kmeans = KMeans(init="random",n_clusters=5,n_init=10,max_iter=300,random_state=42)
kmeans.fit(scaled_features)
centers = kmeans.cluster_centers_

clusterLabels=[]
for i in range(centers.shape[0]):
    cluster = centers[i,:]
    significantCorrelations = zip([x[1] for x in zip(cluster, df.columns) if x[0]> cluster.mean()],[x for x in  cluster if x> cluster.mean()])
    sortedSignificantCorrelations = sorted(list(significantCorrelations),key = lambda x : x[1])
    sortedSignificantCorrelations = sortedSignificantCorrelations[-35:] # don't take last ones, too much too graph and low correlations
    x , y = list(zip(*sortedSignificantCorrelations))
    if "Elise" in x:
        clusterLabels.append("Jungle")
    elif "Ashe" in x:
        clusterLabels.append("Marksman")
    elif "Azir" in x:
        clusterLabels.append("Mid")
    elif "Malphite" in x:
        clusterLabels.append("top")
    elif "Soraka" in x:
        clusterLabels.append("Support")
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.title(clusterLabels[-1])
    plt.show()

#pyplot
patches, texts = plt.pie([x[1] for x in sorted(Counter(kmeans.labels_).items(),key = lambda x: x[0])],  startangle=90)
plt.legend( patches, clusterLabels, loc="best")
plt.show()
#Hierarchical clustering

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)










# hierarchicalModel = AgglomerativeClustering(n_clusters=None, affinity='euclidean', linkage='ward',distance_threshold=1)
# hierarchicalLables = hierarchicalModel.fit_predict(scaled_features)
# plt.title('Hierarchical Clustering Dendrogram')
# # plot the top three levels of the dendrogram
# plot_dendrogram(hierarchicalModel, truncate_mode='level', p=3)
# plt.xlabel("Number of points in node (or index of point if no parenthesis).")
# plt.show()
print("done")