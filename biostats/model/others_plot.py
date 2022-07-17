import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def process(data):
    for col in data:
        try: 
            data[col] = data[col].astype('float64')
        except:
            pass  
    data.columns = data.columns.map(str)
    data.index = data.index.map(str)


def lda_plot(data, x, y):

    sns.set_theme()
    process(data)

    data = data.dropna()

    clf = LinearDiscriminantAnalysis()
    clf.fit(data[x], data[y])

    lda = clf.transform(data[x])
    
    if lda.shape[1] < 2:
        data["ld_1"] = lda[:,0]
        fig, ax = plt.subplots()
        sns.stripplot(data=data, x="ld_1", y=y, hue=y, ax=ax)
        ax.set(xlabel="LD 1")
    else:
        data["ld_1"] = lda[:,0]
        data["ld_2"] = lda[:,1]
        fig, ax = plt.subplots()
        sns.scatterplot(data=data, x="ld_1", y="ld_2", hue=y, ax=ax)
        ax.set(xlabel="LD 1 ({}%)".format(round(clf.explained_variance_ratio_[0]*100,1)))
        ax.set(ylabel="LD 2 ({}%)".format(round(clf.explained_variance_ratio_[1]*100,1)))
        
    return fig

def pca_plot(data, x, color=None):

    sns.set_theme()
    process(data)

    data = data.dropna()

    #for var in x:
    #    data[var] = (data[var] - data[var].mean()) / data[var].std()

    clf = PCA()
    clf.fit(data[x])

    pca = clf.transform(data[x])
    
    if pca.shape[1] < 2:
        data["pc_1"] = pca[:,0]
        fig, ax = plt.subplots()
        sns.stripplot(data=data, x="pc_1", y=color, hue=color, ax=ax)
        ax.set(xlabel="PC 1")
    else:
        data["pc_1"] = pca[:,0]
        data["pc_2"] = pca[:,1]
        fig, ax = plt.subplots()
        sns.scatterplot(data=data, x="pc_1", y="pc_2", hue=color, ax=ax)
        ax.set(xlabel="PC 1 ({}%)".format(round(clf.explained_variance_ratio_[0]*100,1)))
        ax.set(ylabel="PC 2 ({}%)".format(round(clf.explained_variance_ratio_[1]*100,1)))
        
    return fig
