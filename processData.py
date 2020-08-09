from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import skbio

from skbio.stats.composition import ilr, ilr_inv, clr, _gram_schmidt_basis,clr_inv,closure
from helper import multiplicativeReplacementOfZeros
from tqdm import tqdm

from skbio import TreeNode
# from gneiss.balances import balanceplot, balance_basis
# from gneiss.layouts import barchart_layout
import scipy
from functools import partial
tqdm.pandas()

df = pd.read_csv("mainData.csv")


df=df.drop("summoner",axis=1)
minCPfilter  = 	21600 #mastery 5 
df= df[df.max(axis=1)>minCPfilter] #remove players with all champs below some mastery level
replacement_val = df.values[df.values>0].min() #minimum nonzero mastery points 
df = df.progress_apply(lambda x :multiplicativeReplacementOfZeros(x,inputeVal=replacement_val),axis=1) 
df = df.div(df.sum(axis=1), axis=0) # normalize each players stats by sum of row, so get percentage mastery

clrVals = clr(df.values)





def phiMetric(npArray):
    nColumns=npArray.shape[-1]
    tempArray = np.zeros(shape=(nColumns,nColumns))
    clrVals=clr(npArray)
    for i in range(nColumns):
        for j in range(nColumns):
            columnI = clrVals[:,i]
            columnJ = clrVals[:,j]
            tempArray[i,j] = (columnI-columnJ).var()/columnI.var()
    
    #make symmetric
    
    i_lower = np.tril_indices(tempArray.shape[0])
    tempArray[i_lower] =tempArray.T[i_lower]
    return tempArray

def rhoMetric(npArray):
    nColumns=npArray.shape[-1]
    tempArray = np.zeros(shape=(nColumns,nColumns))
    clrVals=clr(npArray)
    for i in range(nColumns):
        for j in range(nColumns):
            columnI = clrVals[:,i]
            columnJ = clrVals[:,j]
            tempArray[i,j] = 1-(columnI-columnJ).var()/(columnI.var()+columnJ.var())


  
    return tempArray


rhoDf = pd.DataFrame(data=rhoMetric(df.values),index=df.columns,columns=df.columns)
rhoDf.to_csv("rhoDf.csv")
phiDf= pd.DataFrame(data=phiMetric(df.values),index=df.columns,columns=df.columns)
phiDf.to_csv("phiDf.csv")
print("done")







