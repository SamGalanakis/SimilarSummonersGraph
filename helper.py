import numpy as np


#turns out scikit-bio has it's own implementation of this : multiplicative_replacement
def replaceVal(val,nZeros,sumRow,inputeVal):
    if val == 0:
        return inputeVal
    return (1- nZeros*inputeVal/sumRow)*val
def multiplicativeReplacementOfZeros(row,inputeVal):
    sumRow=row.sum()
    nZeros = (row==0).sum()
    return row.map(lambda x: replaceVal(x,nZeros,sumRow,inputeVal))