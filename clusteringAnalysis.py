import pandas as pd
from skbio.stats.composition import ilr, ilr_inv, clr, _gram_schmidt_basis,clr_inv,closure
from sklearn.cluster import KMeans, spectral_clustering
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
from helper import multiplicativeReplacementOfZeros
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering, SpectralClustering, FeatureAgglomeration
import numpy as np
from collections import Counter
from scipy.cluster.hierarchy import ward, fcluster, cophenet
from scipy.spatial.distance import pdist
import scipy.cluster.hierarchy as sch
import seaborn as sns
tqdm.pandas()

makeGraphs = True# set to true to produce graphs
sns.set_style("darkgrid")

df=pd.read_csv("data//processedDf.csv",index_col=[0])

rhoDf = pd.read_csv("data//rhoDf.csv",index_col=[0])

clrVals = clr(df.values)

#scale features 
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df.values)
    


# featureKMeans = FeatureAgglomeration(distance_threshold=0, n_clusters=None)
# featureKMeans.fit(scaled_features)
# centers = featureKMeans.cluster_centers_


#Kmeans clustering
kmeans = KMeans(init="random",n_clusters=5,n_init=20,max_iter=1000,random_state=42)
kmeans.fit(scaled_features)

centers = kmeans.cluster_centers_




clusterLabels=[]
for i in range(centers.shape[0]):
    cluster = centers[i,:]
    significantCorrelations = zip([x[1] for x in zip(cluster, df.columns) if x[0]> cluster.mean()],[x for x in  cluster if x> cluster.mean()])
    sortedSignificantCorrelations = sorted(list(significantCorrelations),key = lambda x : x[1])
    sortedSignificantCorrelations = sortedSignificantCorrelations[-20:] # don't take last ones, too much too graph and low correlations
    x , y = list(zip(*sortedSignificantCorrelations))

    if makeGraphs:
        plt.bar(x,y)
        plt.xticks(rotation=45)
        plt.show()
        clusterLabels.append(input("EnterCategorizationOfCluster: "))

#pyplot
if makeGraphs:
    patches, texts = plt.pie([x[1] for x in sorted(Counter(kmeans.labels_).items(),key = lambda x: x[0])],  startangle=90)
    plt.legend( patches, clusterLabels, loc="best")
    plt.show()




    #Make dendrogram
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(clrVals.T)


    linked = linkage(scaled_features, 'ward')

    labels = df.columns.tolist()

    plt.figure(figsize=(14,6))
    plt.title('Hierarchical Clustering Champion Dendrogram', fontsize=20)
    plt.xlabel('Champions', fontsize=16)
    plt.ylabel('Distance', fontsize=16)

    # call dendrogram to get the returned dictionary 
    # (plotting parameters can be ignored at this point)
    R = dendrogram(
                    linked,
                    no_plot=True,
                    )

    print("values passed to leaf_label_func\nleaves : ", R["leaves"])

    # create a label dictionary
    temp = {R["leaves"][ii]: labels[R["leaves"][ii]] for ii in range(len(R["leaves"]))}
    def llf(xx):
        return temp[xx]




    dendrogram(
                linked, 
                color_threshold=0.3*max(linked[:,2]), # to get individual colouring of lower trees but not all the way down
                leaf_label_func=llf,
                leaf_rotation=90.,
                leaf_font_size=8.,
                show_contracted=True,  # to get a distribution impression in truncated branches
                )
    plt.show()