import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import numpy as np

def process(data):
    for col in data:
        try: 
            data[col] = data[col].astype('float64')
        except:
            pass  


'''
data = pd.read_csv("biostats/dataset/one_way_anova.csv", dtype=object)
#data = pd.read_csv("biostats/dataset/penguins.csv", dtype=object)
process(data)

sns.set_theme()

sns.pairplot(data)

#ax = sns.stripplot(x="Location", y="Length", data=data)


fig, axs= plt.subplots(2,2)
sns.stripplot(x="Location", y="Length", data=data, ax=axs[0,0])
sns.swarmplot(x="Location", y="Length", data=data, ax=axs[0,1])
sns.stripplot(x="Location", y="Length", data=data, ax=axs[1,0])
sns.swarmplot(x="Location", y="Length", data=data, ax=axs[1,1])

m = 2
n = 2

for i in range(m):
    for j in range (n):
        if i != m-1:
            axs[i,j].set_xlabel("")
            axs[i,j].set_xticklabels([])
        if j != 0:
            axs[i,j].set_ylabel("")
            axs[i,j].set_yticklabels([])
        plt.sca(axs[i,j])
        plt.xticks(rotation=90)


fig.subplots_adjust(wspace=0.02, hspace=0.02)

plt.show()
'''

data = pd.read_csv("biostats/dataset/one_way_anova.csv", dtype=object)
process(data)
col = data["Length"].to_numpy() * 100 + np.random.normal(20, 20, len(data))

data["Weight"] = data["Length"].to_numpy() * 1000 + np.random.normal(100, 20, len(data))

data["Weight"] = data["Weight"].round(2)

print(data)

data.to_csv('ttt.csv', index=False)
