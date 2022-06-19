import numpy as np
import pandas as pd
from scipy import stats as st

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

def kruskal_wallis_test(data, variable, between):

    process(data)

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

    N = len(data2)
    R_i = data2.groupby(between, sort=False)[variable].sum().tolist()
    n_i = data2.groupby(between, sort=False)[variable].count().tolist()
    k = len(n_i)

    H = 0
    for i in range(k):
        H += R_i[i] * R_i[i] / n_i[i]
    H *= 12 / (N * (N + 1))
    H -= 3 * (N + 1)

    t_i = data2.groupby(variable, sort=False)[variable].count().tolist()
    
    T = 0
    for t in t_i:
        if t > 1:
            T += t ** 3 - t
    H /= 1 - T / (N ** 3 - N)

    p = CC(lambda: 1 - st.chi2.cdf(H, k-1))

    result = pd.DataFrame(
        {
            "D.F.": [k-1],
            "Chi Square": [H],
            "p-value": [p]
        }, index=["Model"]
    )

    add_p(result)

    process(summary)
    process(result)

    return summary, result