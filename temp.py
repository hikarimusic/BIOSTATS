import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import numpy as np
from scipy import stats as st

def process(data):
    for col in data:
        try: 
            data[col] = data[col].astype('float64')
        except:
            pass  
    data.columns = data.columns.map(str)
    data.index = data.index.map(str)


'''
data = bs.dataset("one_way_anova.csv", dtype=object)
#data = bs.dataset("penguins.csv", dtype=object)
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

data = bs.dataset("one_way_anova.csv", dtype=object)
process(data)
col = data["Length"].to_numpy() * 100 + np.random.normal(20, 20, len(data))

data["Weight"] = data["Length"].to_numpy() * 1000 + np.random.normal(100, 20, len(data))

data["Weight"] = data["Weight"].round(2)

print(data)

data.to_csv('ttt.csv', index=False)

data = pd.DataFrame(columns=["Genotype", "Health"])

for i in range (268):
    aaa = pd.DataFrame({"Genotype":["ins-ins"], "Health":["no_disease"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

for i in range (807):
    aaa = pd.DataFrame({"Genotype":["ins-ins"], "Health":["disease"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

for i in range (199):
    aaa = pd.DataFrame({"Genotype":["ins-del"], "Health":["no_disease"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

for i in range (759):
    aaa = pd.DataFrame({"Genotype":["ins-del"], "Health":["disease"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

for i in range (42):
    aaa = pd.DataFrame({"Genotype":["del-del"], "Health":["no_disease"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

for i in range (184):
    aaa = pd.DataFrame({"Genotype":["del-del"], "Health":["disease"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

data = data.sample(frac=1).reset_index(drop=True)

data.to_csv('ttt.csv', index=False)

print(data)

table = np.array([[43, 44, 49], [7, 6, 1]])

oddsr, p = st.fisher_exact(table, alternative='two-sided')

print(p)
'''

'''
import math

def _dfs(mat, pos, r_sum, c_sum, p_0, p):

    (xx, yy) = pos
    (r, c) = (len(r_sum), len(c_sum))

    mat_new = []

    for i in range(len(mat)):
        temp = []
        for j in range(len(mat[0])):
            temp.append(mat[i][j])
        mat_new.append(temp)

    if xx == -1 and yy == -1:
        for i in range(r-1):
            temp = r_sum[i]
            for j in range(c-1):
                temp -= mat_new[i][j]
            mat_new[i][c-1] = temp
        for j in range(c-1):
            temp = c_sum[j]
            for i in range(r-1):
                temp -= mat_new[i][j]
            mat_new[r-1][j] = temp
        temp = r_sum[r-1]
        for j in range(c-1):
            temp -= mat_new[r-1][j]
        if temp <0:
            return
        mat_new[r-1][c-1] = temp

        p_1 = 1
        for x in r_sum:
            p_1 *= math.factorial(x)
        for y in c_sum:
            p_1 *= math.factorial(y)

        n = 0
        for x in r_sum:
            n += x
        p_1 /= math.factorial(n)

        for i in range(len(mat_new)):
            for j in range(len(mat_new[0])):
                p_1 /= math.factorial(mat_new[i][j])
        if p_1 <= p_0 + 0.00000001:
            #print(mat_new)
            #print(p_1)
            p[0] += p_1
    else:
        max_1 = r_sum[xx]
        max_2 = c_sum[yy]
        for j in range(c):
            max_1 -= mat_new[xx][j]
        for i in range(r):
            max_2 -= mat_new[i][yy]
        for k in range(min(max_1,max_2)+1):
            mat_new[xx][yy] = k
            if xx == r-2 and yy == c-2:
                pos_new = (-1, -1)
            elif xx == r-2:
                pos_new = (0, yy+1)
            else:
                pos_new = (xx+1, yy)
            _dfs(mat_new, pos_new, r_sum, c_sum, p_0, p)


def fisher_exact(table):

    row_sum = []
    col_sum = []

    for i in range(len(table)):
        temp = 0
        for j in range(len(table[0])):
            temp += table[i][j]
        row_sum.append(temp)
    
    for j in range(len(table[0])):
        temp = 0
        for i in range(len(table)):
            temp += table[i][j]
        col_sum.append(temp)

    mat = [[0] * len(col_sum)] * len(row_sum)
    pos = (0, 0)

    p_0 = 1

    for x in row_sum:
        p_0 *= math.factorial(x)
    for y in col_sum:
        p_0 *= math.factorial(y)

    n = 0
    for x in row_sum:
        n += x
    p_0 /= math.factorial(n)

    for i in range(len(table)):
        for j in range(len(table[0])):
            p_0 /= math.factorial(table[i][j])

    p = [0]
    _dfs(mat, pos, row_sum, col_sum, p_0, p)

    return p[0]


print(fisher_exact([[1,24],[5,20],[14,11],[11,14]]))
#fisher_exact([[16,8],[3,18]])
#fisher_exact([[43,2],[17,7]])
#fisher_exact([[43,7],[44,6],[49,1]])
#fisher_exact([[127,116],[99,67],[264,161]])
#fisher_exact([[15,8],[20,5],[14,7],[6,1]])


#fisher_exact([[3,9],[13,4]])
#fisher_exact([[43,7],[44,6],[49,1]])
#fisher_exact([[43,44,49],[7,6,1], [2,3,4]])
#isher_exact([[2,2],[2,2],[2,2]])
'''

'''
data = pd.DataFrame(columns=["Frequency", "Result"])

for i in range (1):
    aaa = pd.DataFrame({"Frequency":["Daily"], "Result":["Damaged"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

for i in range (5):
    aaa = pd.DataFrame({"Frequency":["Weekly"], "Result":["Damaged"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

for i in range (14):
    aaa = pd.DataFrame({"Frequency":["Monthly"], "Result":["Damaged"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

for i in range (11):
    aaa = pd.DataFrame({"Frequency":["Quarterly"], "Result":["Damaged"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

for i in range (24):
    aaa = pd.DataFrame({"Frequency":["Daily"], "Result":["Undamaged"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

for i in range (20):
    aaa = pd.DataFrame({"Frequency":["Weekly"], "Result":["Undamaged"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

for i in range (11):
    aaa = pd.DataFrame({"Frequency":["Monthly"], "Result":["Undamaged"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

for i in range (14):
    aaa = pd.DataFrame({"Frequency":["Quarterly"], "Result":["Undamaged"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

data = data.sample(frac=1).reset_index(drop=True)

data.to_csv('ttt.csv', index=False)

print(data)
'''



str = '''
Group      Value
Group.1      1
Group.1      2
Group.1      3
Group.1      4
Group.1      5
Group.1      6
Group.1      7
Group.1      8
Group.1      9
Group.1     46
Group.1     47
Group.1     48
Group.1     49
Group.1     50
Group.1     51
Group.1     52
Group.1     53
Group.1    342
Group.2     10
Group.2     11
Group.2     12
Group.2     13
Group.2     14
Group.2     15
Group.2     16
Group.2     17
Group.2     18
Group.2     37
Group.2     58
Group.2     59
Group.2     60
Group.2     61
Group.2     62
Group.2     63
Group.2     64
Group.2    193
Group.3     19
Group.3     20
Group.3     21
Group.3     22
Group.3     23
Group.3     24
Group.3     25
Group.3     26
Group.3     27
Group.3     28
Group.3     65
Group.3     66
Group.3     67
Group.3     68
Group.3     69
Group.3     70
Group.3     71
Group.3     72
'''

'''
str = str.replace("\n", "!")
str = str.split()
str = ",".join(str)
str = str.replace("!", "\n")

with open("test.txt", "w") as f:
    f.write(str)
'''


data = pd.DataFrame(columns=["Color"])


for i in range (35):
    aaa = pd.DataFrame({"Color":["Red"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

for i in range (74):
    aaa = pd.DataFrame({"Color":["Yellow"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

for i in range (22):
    aaa = pd.DataFrame({"Color":["Green"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

for i in range (69):
    aaa = pd.DataFrame({"Color":["Blue"]})
    data = pd.concat([data, aaa], ignore_index=True, axis=0)

data = data.sample(frac=1).reset_index(drop=True)

size = ["Small"] * 67 + ["Middle"] * 102 + ["Large"] * 31

data["size"] = size

data = data.sample(frac=1).reset_index(drop=True)

data.to_csv('categorical.csv', index=False)

