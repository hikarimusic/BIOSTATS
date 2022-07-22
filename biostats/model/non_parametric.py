import numpy as np
import pandas as pd
from scipy import stats as st
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


class permutation:

    def __init__(self, N, n):
        self.N = N
        self.n = n
        self.s_0 = 0
        self.s_1 = 0
    
    def calc(self):
        self.dfs(0, 1)
        return self.s_1 / self.s_0

    def dfs(self, s, i):
        if i == self.N+1:
            self.s_0 += 1
            if s <= self.n:
                self.s_1 += 1
        else:
            self.dfs(s, i+1)
            self.dfs(s+i, i+1)


def median_test(data, variable, expect):

    process(data)
    data = data[[variable]].dropna()

    if str(data[variable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(variable))

    summary = pd.DataFrame(
        {
            "Count": CC(data[variable].count),
            "Mean": CC(data[variable].mean),
            "Std. Deviation": CC(data[variable].std,),
            "Minimum": CC(data[variable].min),
            "1st Quartile": CC(lambda: data[variable].quantile(0.25)),
            "Median": CC(data[variable].median),
            "3rd Quartile": CC(lambda: data[variable].quantile(0.75)),
            "Maximum": CC(data[variable].max),
        }, index=[variable]
    )

    data_wide = pd.DataFrame(
        {
            "var_1" : data[variable].dropna().tolist() ,
            "var_2" : [expect] * len(data[variable].dropna())
        }
    )
    data_wide["diff"] = data_wide["var_1"] - data_wide["var_2"]
    data_wide = data_wide.drop(data_wide[data_wide["diff"] == 0].index)
    data_wide["abs"] = data_wide["diff"].abs()
    data_wide["rank"] = data_wide["abs"].rank()

    n = CC(lambda: len(data_wide))
    R = CC(lambda: data_wide[data_wide["diff"] > 0]["rank"].sum())
    if R == CC(lambda: n * (n+1) / 4):
        T = 0
    else:
        _t = data_wide["abs"].value_counts().tolist()
        _tsum = 0
        for x in _t:
            _tsum = CC(lambda: _tsum + x**3 - x)
        T = CC(lambda: (abs(R - n * (n+1) / 4) - 0.5) / math.sqrt(n * (n+1) * (2*n+1) / 24 - _tsum / 48))
    p = CC(lambda: 2 * (1 - st.norm.cdf(T)))

    if n < 15:
        exact = permutation(n, int(R))
        _p = CC(lambda: exact.calc())
        _p = CC(lambda: 2 * min(_p, 1-_p))
    else:
        _p = np.nan
    
    result = pd.DataFrame(
        {
            "Rank Sum" : [R, R] ,
            "z Statistic" : [T, None] ,
            "p-value" : [p, _p]
        }, index=["Normal", "Exact"]
    )
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def sign_test(data, variable, between, group, pair):

    process(data)
    data = data[list({variable, between, pair})].dropna()

    if str(data[variable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))
    if data[pair].nunique() > 2000:
        raise Warning("The nmuber of classes in column '{}' cannot > 2000.".format(pair))

    data = data[data[between].isin(group)]
    cross = pd.crosstab(index=data[pair], columns=data[between])
    for col in cross:
        cross = cross.drop(cross[cross[col] != 1].index)
    sub = cross.index.values.tolist()
    data = data[data[pair].isin(sub)]

    summary = pd.DataFrame(
        {
            "Count": CC(data.groupby(between, sort=False)[variable].count),
            "Mean": CC(data.groupby(between, sort=False)[variable].mean),
            "Std. Deviation": CC(data.groupby(between, sort=False)[variable].std,),
            "Minimum": CC(data.groupby(between, sort=False)[variable].min),
            "1st Quartile": CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.25)),
            "Median": CC(data.groupby(between, sort=False)[variable].median),
            "3rd Quartile": CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.75)),
            "Maximum": CC(data.groupby(between, sort=False)[variable].max),
        }
    )
    summary.index.name = None
    summary = summary.reindex(group)

    data_wide = pd.DataFrame(
        {
            "var_1" : data[data[between]==group[0]].sort_values(by=[pair])[variable].tolist() ,
            "var_2" : data[data[between]==group[1]].sort_values(by=[pair])[variable].tolist()
        }
    )
    data_wide["diff"] = data_wide["var_1"] - data_wide["var_2"]
    data_wide = data_wide.drop(data_wide[data_wide["diff"] == 0].index)

    n = CC(lambda: len(data_wide))
    C = CC(lambda: data_wide[data_wide["diff"] > 0]["diff"].count())
    if C == n/2 :
        z = 0
        p = 1
    elif C > n/2 :
        z = CC(lambda: (C- n/2 - 0.5) / math.sqrt(n/4))
        p = CC(lambda: 2 * (1 - st.norm.cdf(z)))
    else :
        z = CC(lambda: (C - n/2 + 0.5) / math.sqrt(n/4))
        p = CC(lambda: 2 * st.norm.cdf(z))

    if n < 20:
        _p = 0
        if C > n/2:
            for x in range(C, n+1):
                _p = CC(lambda: _p + math.factorial(n) / (math.factorial(x) * math.factorial(n-x) * 2**n))
            _p = CC(lambda: _p * 2)
        elif C < n/2:
            for x in range(0, C+1):
                _p = CC(lambda: _p + math.factorial(n) / (math.factorial(x) * math.factorial(n-x) * 2**n))
            _p = CC(lambda: _p * 2)
        else: 
            _p = 1
    else:
        _p = np.nan
    
    result = pd.DataFrame(
        {
            "Sum" : [C, C] ,
            "z Statistic" : [z, None] ,
            "p-value" : [p, _p]
        }, index=["Normal", "Exact"]
    )
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def wilcoxon_signed_rank_test(data, variable, between, group, pair):

    process(data)
    data = data[list({variable, between, pair})].dropna()

    if str(data[variable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))
    if data[pair].nunique() > 2000:
        raise Warning("The nmuber of classes in column '{}' cannot > 2000.".format(pair))

    data = data[data[between].isin(group)]
    cross = pd.crosstab(index=data[pair], columns=data[between])
    for col in cross:
        cross = cross.drop(cross[cross[col] != 1].index)
    sub = cross.index.values.tolist()
    data = data[data[pair].isin(sub)]

    summary = pd.DataFrame(
        {
            "Count": CC(data.groupby(between, sort=False)[variable].count),
            "Mean": CC(data.groupby(between, sort=False)[variable].mean),
            "Std. Deviation": CC(data.groupby(between, sort=False)[variable].std,),
            "Minimum": CC(data.groupby(between, sort=False)[variable].min),
            "1st Quartile": CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.25)),
            "Median": CC(data.groupby(between, sort=False)[variable].median),
            "3rd Quartile": CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.75)),
            "Maximum": CC(data.groupby(between, sort=False)[variable].max),
        }
    )
    summary.index.name = None
    summary = summary.reindex(group)

    data_wide = pd.DataFrame(
        {
            "var_1" : data[data[between]==group[0]].sort_values(by=[pair])[variable].tolist() ,
            "var_2" : data[data[between]==group[1]].sort_values(by=[pair])[variable].tolist()
        }
    )
    data_wide["diff"] = data_wide["var_1"] - data_wide["var_2"]
    data_wide = data_wide.drop(data_wide[data_wide["diff"] == 0].index)
    data_wide["abs"] = data_wide["diff"].abs()
    data_wide["rank"] = data_wide["abs"].rank()

    n = CC(lambda: len(data_wide))
    R = CC(lambda: data_wide[data_wide["diff"] > 0]["rank"].sum())
    if R == CC(lambda: n * (n+1) / 4):
        T = 0
    else:
        _t = data_wide["abs"].value_counts().tolist()
        _tsum = 0
        for x in _t:
            _tsum = CC(lambda: _tsum + x**3 - x)
        T = CC(lambda: (abs(R - n * (n+1) / 4) - 0.5) / math.sqrt(n * (n+1) * (2*n+1) / 24 - _tsum / 48))
    p = CC(lambda: 2 * (1 - st.norm.cdf(T)))

    if n < 15:
        exact = permutation(n, int(R))
        _p = CC(lambda: exact.calc())
        _p = CC(lambda: 2 * min(_p, 1-_p))
    else:
        _p = np.nan
    
    result = pd.DataFrame(
        {
            "Rank Sum" : [R, R] ,
            "z Statistic" : [T, None] ,
            "p-value" : [p, _p]
        }, index=["Normal", "Exact"]
    )
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def wilcoxon_rank_sum_test(data, variable, between, group):

    process(data)
    data = data[list({variable, between})].dropna()

    if str(data[variable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))

    data = data[data[between].isin(group)]
    data = data[data[variable].notna()]
    data["rank"] = data[variable].rank()

    summary = pd.DataFrame(
        {
            "Count": CC(data.groupby(between, sort=False)[variable].count),
            "Mean": CC(data.groupby(between, sort=False)[variable].mean),
            "Std. Deviation": CC(data.groupby(between, sort=False)[variable].std,),
            "Minimum": CC(data.groupby(between, sort=False)[variable].min),
            "1st Quartile": CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.25)),
            "Median": CC(data.groupby(between, sort=False)[variable].median),
            "3rd Quartile": CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.75)),
            "Maximum": CC(data.groupby(between, sort=False)[variable].max),
        }
    )
    summary.index.name = None
    summary = summary.reindex(group)

    n_1 = CC(data[data[between]==group[0]]["rank"].count)
    n_2 = CC(data[data[between]==group[1]]["rank"].count)
    R = CC(data[data[between]==group[0]]["rank"].sum)
    if R == CC(lambda: n_1 * (n_1 + n_2 + 1) / 2) :
        T = 0
    else:
        _t = data["rank"].value_counts().tolist()
        _tsum = 0
        for x in _t:
            _tsum = CC(lambda: _tsum + x**3 - x)
        T = CC(lambda: (abs(R -n_1*(n_1+n_2+1)/2)-0.5)/math.sqrt((n_1*n_2/12)*(n_1+n_2+1-_tsum/((n_1+n_2)*(n_1+ n_2-1)))))
    p = CC(lambda: 2 * (1 - st.norm.cdf(T)))

    if n_1 + n_2 < 15:
        exact = permutation(n_1+n_2, int(R))
        _p = CC(lambda: exact.calc())
        _p = CC(lambda: 2 * min(_p, 1-_p))
    else:
        _p = np.nan

    result = pd.DataFrame(
        {
            "Rank Sum" : [R, R] ,
            "z Statistic" : [T, None] ,
            "p-value" : [p, _p]
        }, index=["Normal", "Exact"]
    )
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def kruskal_wallis_test(data, variable, between):

    process(data)
    data = data[list({variable, between})].dropna()

    if str(data[variable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))

    summary = pd.DataFrame(
        {
            "{}".format(between) : CC(data.groupby(between, sort=False)[variable].groups.keys),
            "Count": CC(data.groupby(between, sort=False)[variable].count),
            "Mean": CC(data.groupby(between, sort=False)[variable].mean),
            "Std. Deviation": CC(data.groupby(between, sort=False)[variable].std,),
            "Minimum": CC(data.groupby(between, sort=False)[variable].min),
            "1st Quartile": CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.25)),
            "Median": CC(data.groupby(between, sort=False)[variable].median),
            "3rd Quartile": CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.75)),
            "Maximum": CC(data.groupby(between, sort=False)[variable].max),
        }
    )

    summary.index.name = None
    summary = summary.reset_index(drop=True)
    summary.index += 1

    data2 = pd.DataFrame()
    data2[variable] = data[variable].rank(method='average')
    data2[between] = data[between]
    data2 = data2.dropna()

    N = CC(lambda: len(data2))
    R_i = data2.groupby(between, sort=False)[variable].sum().tolist()
    n_i = data2.groupby(between, sort=False)[variable].count().tolist()
    k = CC(lambda: len(n_i))

    H = 0
    for i in range(k):
        H = CC(lambda: H + R_i[i] * R_i[i] / n_i[i])
    H = CC(lambda: H * 12 / (N * (N + 1)))
    H = CC(lambda: H - 3 * (N + 1))

    t_i = data2.groupby(variable, sort=False)[variable].count().tolist()
    
    T = 0
    for t in t_i:
        if t > 1:
            T = CC(lambda: T + t ** 3 - t)
    H = CC(lambda: H / (1 - T / (N ** 3 - N)))

    p = CC(lambda: 1 - st.chi2.cdf(H, k-1))

    result = pd.DataFrame(
        {
            "D.F.": CC(lambda: k-1),
            "Chi Square": CC(lambda: H),
            "p-value": CC(lambda: p)
        }, index=["Model"]
    )

    add_p(result)

    process(summary)
    process(result)

    return summary, result


def friedman_test(data, variable, between, subject):

    process(data)
    data = data[list({variable, between, subject})].dropna()

    if str(data[variable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))
    if data[subject].nunique() > 2000:
        raise Warning("The nmuber of classes in column '{}' cannot > 2000.".format(subject))

    cross = pd.crosstab(index=data[subject], columns=data[between])
    for col in cross:
        cross = cross.drop(cross[cross[col] != 1].index)
    sub = cross.index.values.tolist()
    data = data[data[subject].isin(sub)]
    
    group = data[between].dropna().unique()

    summary = pd.DataFrame()

    for x in group:
        temp = pd.DataFrame(
            {
                "{}".format(between): x,
                "Count": CC(data[data[between]==x][variable].dropna().count) ,
                "Mean": CC(data[data[between]==x][variable].dropna().mean) ,
                "Std. Deviation": CC(data[data[between]==x][variable].dropna().std) ,
                "Minimum": CC(data[data[between]==x][variable].dropna().min),
                "1st Quartile": CC(lambda: data[data[between]==x][variable].dropna().quantile(0.25)),
                "Median": CC(data[data[between]==x][variable].dropna().median),
                "3rd Quartile": CC(lambda: data[data[between]==x][variable].dropna().quantile(0.75)),
                "Maximum": CC(data[data[between]==x][variable].dropna().max),
            }, index=[0]
        )
        summary = pd.concat([summary, temp], ignore_index=True)
    summary.index += 1

    data_wide = pd.DataFrame()
    for x in group:
        data_wide[x] = data[data[between]==x].sort_values(by=[subject])[variable].tolist()
    data_wide = data_wide.rank(axis=1)

    k = CC(lambda: len(data_wide.columns))
    n = CC(lambda: len(data_wide))
    R_2 = 0
    for col in data_wide.columns:
        r = CC(lambda: data_wide[col].sum())
        R_2 = CC(lambda: R_2 + r * r)
    chi2 = CC(lambda: R_2 * 12 / (n * k * (k + 1)) - 3 * n * (k + 1))
    p = CC(lambda: 1 - st.chi2.cdf(chi2, k-1))

    result = pd.DataFrame(
        {
            "D.F.": CC(lambda: k-1),
            "Chi Square": CC(lambda: chi2),
            "p-value": CC(lambda: p)
        }, index=["Model"]
    )
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def spearman_rank_correlation(data, x, y):

    process(data)
    data = data[list({x, y})].dropna()

    if str(data[x].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(x))
    if str(data[y].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(y))

    data = data[[x,y]].dropna()
    data["rank_x"] = data[x].rank()
    data["rank_y"] = data[y].rank()
    data = data[["rank_x", "rank_y"]]
    r = CC(lambda: data.corr().iloc[0][1])
    n = CC(lambda: len(data))

    summary = pd.DataFrame(
        {
            "Coefficient": CC(lambda: r)
        }, index=["Correlation"]
    )

    t = CC(lambda: r * math.sqrt((n - 2) / (1 - r * r)))
    p = CC(lambda: st.t.cdf(t, n-2))
    p = CC(lambda a: 2*min(a, 1-a), p)

    result = pd.DataFrame(
        {
            "D.F." : CC(lambda: n-2) ,
            "t Statistic" : CC(lambda: t) ,
            "p-value" : CC(lambda: p)
        }, index=["Model"]
    )
    add_p(result)

    process(summary)
    process(result)

    return summary, result