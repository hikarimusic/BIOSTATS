import numpy as np
import pandas as pd
import math

def CC(fun, *args):
    try:
        return fun(*args)
    except:
        return np.nan

def process(data):
    for col in data:
        try: 
            data[col] = data[col].astype('float64')
        except:
            pass  
    data.columns = data.columns.map(str)
    data.index = data.index.map(str)

def add_p(data):
    temp = [np.nan] * len(data)
    for i in range(len(data)):
        if data['p-value'][i] <= 0.05:
            temp[i] = "*"
        if data['p-value'][i] <= 0.01:
            temp[i] = "**"
        if data['p-value'][i] <= 0.001:
            temp[i] = "***"
    data[""] = temp

class binom_exact:

    def __init__(self, table, freqency):
        self.table = table
        self.freq = freqency

    def calc(self):

        self.sum = sum(self.table)

        self.p_part = math.factorial(self.sum)

        self.p_0 = self.multi_nom(self.table)
        self.p = 0
        #self.cnt = 0

        mat = [0] * len(self.table)
        pos = 0

        self.dfs(mat, pos)

        #if self.cnt > 1000000:
        #    return np.NAN

        return self.p

    def dfs(self, mat, pos):

        #self.cnt += 1
        #if self.cnt > 1000000:
        #    return

        mat_new = []
        for x in mat:
            mat_new.append(x)

        if pos == -1:
            temp = self.sum - sum(mat_new)
            if temp <0:
                return
            mat_new[len(mat)-1] = temp

            p_1 = self.multi_nom(mat_new)
            if p_1 <= self.p_0 + 0.000000000000000001:
                self.p += p_1
        else:
            max_ = self.sum - sum(mat_new)
            for k in range(max_+1):
                mat_new[pos] = k
                if pos == len(mat)-2:
                    pos_new = -1
                else:
                    pos_new = pos + 1
                self.dfs(mat_new, pos_new)

    def multi_nom(self, table):
        p = self.p_part
        for i in range(len(table)):
            p *= self.freq[i] ** table[i]
        for x in table:
            p /= math.factorial(x)
        return p

def binomial_test(data, variable, expect):
    
    process(data)
    data = data[[variable]].dropna()

    if data[variable].nunique() > 10:
        raise Warning("The nmuber of classes in column '{}' cannot > 10.".format(variable))
    if len(data) > 500:
        raise Warning("The length of data cannot > 500.")

    cat = data.groupby(variable, sort=False)[variable].groups.keys()
    obs = []
    exp = []
    for var in cat:
        CC(lambda: obs.append(data[variable].value_counts()[var]))
    exp_val = list(expect.values())
    for var in cat:
        CC(lambda: exp.append(expect[var] / sum(exp_val)))

    summary = pd.DataFrame(
        {
            "Observe" : CC(lambda: obs),
            "Expect"  : CC(lambda: exp)
        }, index=cat
    )

    test = binom_exact(obs, exp)
    p = CC(lambda: test.calc())

    result = pd.DataFrame(
        {
            "p-value": CC(lambda: p)
        }, index=["Model"]
    )

    add_p(result)

    process(summary)
    process(result)

    return summary, result

class fisher_exact:
    
    def __init__(self, table):
        self.table = table

    def calc(self):

        self.row_sum = []
        self.col_sum = []
        self.sum = 0

        for i in range(len(self.table)):
            temp = 0
            for j in range(len(self.table[0])):
                temp += self.table[i][j]
            self.row_sum.append(temp)
        
        for j in range(len(self.table[0])):
            temp = 0
            for i in range(len(self.table)):
                temp += self.table[i][j]
            self.col_sum.append(temp)
        
        for k in self.row_sum:
            self.sum += k
        
        self.p_part = 1
        for x in self.row_sum:
            self.p_part *= math.factorial(x)
        for y in self.col_sum:
            self.p_part *= math.factorial(y)
        self.p_part /= math.factorial(self.sum)

        self.p_0 = self.hyper_geom(self.table)
        self.p = 0
        #self.cnt = 0

        mat = [[0] * len(self.col_sum)] * len(self.row_sum)
        pos = (0, 0)

        self.dfs(mat, pos)

        #if self.cnt > 1000000:
        #    return np.NAN

        return self.p

    def dfs(self, mat, pos):

        #self.cnt += 1
        #if self.cnt > 1000000:
        #    return
        
        (xx, yy) = pos
        (rr, cc) = (len(self.row_sum), len(self.col_sum))

        mat_new = []

        for i in range(len(mat)):
            temp = []
            for j in range(len(mat[0])):
                temp.append(mat[i][j])
            mat_new.append(temp)

        if xx == -1 and yy == -1:
            for i in range(rr-1):
                temp = self.row_sum[i]
                for j in range(cc-1):
                    temp -= mat_new[i][j]
                mat_new[i][cc-1] = temp
            for j in range(cc-1):
                temp = self.col_sum[j]
                for i in range(rr-1):
                    temp -= mat_new[i][j]
                mat_new[rr-1][j] = temp
            temp = self.row_sum[rr-1]
            for j in range(cc-1):
                temp -= mat_new[rr-1][j]
            if temp <0:
                return
            mat_new[rr-1][cc-1] = temp
            
            p_1 = self.hyper_geom(mat_new)

            if p_1 <= self.p_0 + 0.000000000000000001:
                self.p += p_1
        else:
            max_1 = self.row_sum[xx]
            max_2 = self.col_sum[yy]
            for j in range(cc):
                max_1 -= mat_new[xx][j]
            for i in range(rr):
                max_2 -= mat_new[i][yy]
            for k in range(min(max_1,max_2)+1):
                mat_new[xx][yy] = k
                if xx == rr-2 and yy == cc-2:
                    pos_new = (-1, -1)
                elif xx == rr-2:
                    pos_new = (0, yy+1)
                else:
                    pos_new = (xx+1, yy)
                self.dfs(mat_new, pos_new)

    def hyper_geom(self, table):
        p = self.p_part
        for i in range(len(table)):
            for j in range(len(table[0])):
                p /= math.factorial(table[i][j])
        return p

def fisher_exact_test(data, variable_1, variable_2):
    
    process(data)
    data = data[list({variable_1, variable_2})].dropna()

    if data[variable_1].nunique() > 10:
        raise Warning("The nmuber of classes in column '{}' cannot > 10.".format(variable_1))
    if data[variable_2].nunique() > 10:
        raise Warning("The nmuber of classes in column '{}' cannot > 10.".format(variable_2))
    if data[variable_2].nunique() > 10:
        raise Warning("The nmuber of classes in column '{}' cannot > 10.".format(variable_2))

    summary = pd.crosstab(index=data[variable_1], columns=data[variable_2])
    summary.index.name = None
    summary.columns.name = None

    test = fisher_exact(summary.values.tolist())
    p = CC(lambda: test.calc())

    result = pd.DataFrame(
        {
            "p-value": CC(lambda: p)
        }, index=["Model"]
    )
    
    add_p(result)

    process(summary)
    process(result)

    return summary, result

def mcnemar_exact_test(data, variable_1, variable_2, pair):

    process(data)
    data = data[list({variable_1, variable_2, pair})].dropna()

    if data[variable_1].nunique() > 10:
        raise Warning("The nmuber of classes in column '{}' cannot > 10.".format(variable_1))
    if data[variable_2].nunique() > 10:
        raise Warning("The nmuber of classes in column '{}' cannot > 10.".format(variable_2))
    if data[pair].nunique() > 1000:
        raise Warning("The nmuber of classes in column '{}' cannot > 1000.".format(pair))

    grp_1 = data[variable_1].value_counts()[:2].index.tolist()
    grp_2 = data[variable_2].value_counts()[:2].index.tolist()

    data = data[data[variable_1].isin(grp_1)]
    data = data[data[variable_2].isin(grp_2)]

    cross = pd.crosstab(index=data[pair], columns=data[variable_1])
    for col in cross:
        cross = cross.drop(cross[cross[col] != 1].index)
    sub = cross.index.values.tolist()
    data = data[data[pair].isin(sub)]

    _dat = pd.DataFrame(
        {
            "fst" : data[data[variable_1]==grp_1[0]].sort_values(by=[pair])[variable_2].tolist() ,
            "snd" : data[data[variable_1]==grp_1[1]].sort_values(by=[pair])[variable_2].tolist()
        }
    )

    a = CC(lambda: _dat[(_dat["fst"]==grp_2[0]) & (_dat["snd"]==grp_2[0])]["fst"].count())
    b = CC(lambda: _dat[(_dat["fst"]==grp_2[0]) & (_dat["snd"]==grp_2[1])]["fst"].count())
    c = CC(lambda: _dat[(_dat["fst"]==grp_2[1]) & (_dat["snd"]==grp_2[0])]["fst"].count())
    d = CC(lambda: _dat[(_dat["fst"]==grp_2[1]) & (_dat["snd"]==grp_2[1])]["fst"].count())

    summary = pd.DataFrame(
        {
            "{} : {}".format(grp_1[1], grp_2[0]) : [a, c] ,
            "{} : {}".format(grp_1[1], grp_2[1]) : [b, d] ,
        }, index=["{} : {}".format(grp_1[0], grp_2[0]), "{} : {}".format(grp_1[0], grp_2[1])]
    )

    p = CC(lambda: 0)
    n = CC(lambda: b + c)
    if b < c:
        for x in range(0, b+1):
            p = CC(lambda: p + math.factorial(n) / (math.factorial(x) * math.factorial(n-x) * 2**n))
        p = CC(lambda: p * 2)
    elif b > c:
        for x in range(b, n+1):
            p = CC(lambda: p + math.factorial(n) / (math.factorial(x) * math.factorial(n-x) * 2**n))
        p = CC(lambda: p * 2)
    else: 
        p = CC(lambda: 1)

    result = pd.DataFrame(
        {
            "p-value": CC(lambda: p)
        }, index=["Model"]
    )
    add_p(result)

    process(summary)
    process(result)

    return summary, result