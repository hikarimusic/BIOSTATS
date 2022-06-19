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

def chi_square_test(data, variable_1, variable_2):
    
    process(data)

    summary = pd.crosstab(index=data[variable_1], columns=data[variable_2])
    summary.index.name = None
    summary.columns.name = None

    obs = summary.values.tolist()

    rr = len(obs)
    cc = len(obs[0])
    r_sum = []
    c_sum = []
    _sum = 0

    for i in range(rr):
        temp = 0
        for j in range(cc):
            temp += obs[i][j]
        r_sum.append(temp)
    for j in range(cc):
        temp = 0
        for i in range(rr):
            temp += obs[i][j]
        c_sum.append(temp)
    for i in range(rr):
        _sum += r_sum[i]
    
    exp = []

    for i in range(rr):
        temp = []
        for j in range(cc):
            temp.append(r_sum[i] * c_sum[j] / _sum)
        exp.append(temp)
    
    chi2 = 0
    for i in range(rr):
        for j in range(cc):
            chi2 += (obs[i][j]-exp[i][j]) ** 2 / exp[i][j]
    
    p = CC(lambda: 1 - st.chi2.cdf(chi2, (rr-1)*(cc-1)))

    result = pd.DataFrame(
        {
            "D.F.": [(rr-1)*(cc-1)],
            "Chi Square": [chi2],
            "p-value": [p]
        }, index=["Normal"]
    )

    if summary.shape == (2,2):
        chi2 = 0
        for i in range(rr):
            for j in range(cc):
                chi2 += (abs(obs[i][j]-exp[i][j])-0.5) ** 2 / exp[i][j]
        
        p = CC(lambda: 1 - st.chi2.cdf(chi2, (rr-1)*(cc-1)))

        result2 = pd.DataFrame(
            {
            "D.F.": [(rr-1)*(cc-1)],
            "Chi Square": [chi2],
            "p-value": [p]
            }, index=["Corrected"]
        )
        result = pd.concat([result, result2], axis=0)
    
    add_p(result)

    process(summary)
    process(result)

    return summary, result

def chi_square_test_fit(data, variable, expect):
    
    process(data)

    cat = data.groupby(variable, sort=False)[variable].groups.keys()
    obs = []
    exp = []
    for var in cat:
        obs.append(data[variable].value_counts()[var])
    exp_val = list(expect.values())
    for var in cat:
        exp.append(expect[var] * sum(obs) / sum(exp_val))
    dim = len(obs)

    summary = pd.DataFrame(
        {
            "Observe" : obs,
            "Expect"  : exp
        }, index=cat
    )

    chi2 = 0
    for i in range(dim):
        chi2 += (obs[i]-exp[i]) * (obs[i]-exp[i]) / exp[i]
    p = CC(lambda: 1 - st.chi2.cdf(chi2, dim-1))
    result = pd.DataFrame(
        {
            "D.F.": [dim-1],
            "Chi Square": [chi2],
            "p-value": [p]
        }, index=["Normal"]
    )

    add_p(result)

    process(summary)
    process(result)

    return summary, result



"""
from scipy.stats import chisquare, chi2_contingency

def chi_square_independence(data, first, second, summary=None):

    table = pd.crosstab(index=data[first], columns=data[second])
    table.index.name = None
    index_change = {}
    for index in table.index:
        changed = "{}({})".format(first, index)
        index_change[index] = changed
    table =  table.rename(index=index_change)
    table.columns.name = None
    columns_change = {}
    for columns in table.columns:
        changed = "{}({})".format(second, columns)
        columns_change[columns] = changed
    table =  table.rename(columns=columns_change)

    chi2, p, df, ex = chi2_contingency(table, False)
    chi2_, p_, df_, ex_, = chi2_contingency(table, True)
    result = pd.DataFrame(
        {
            "Chi_Square": [chi2, chi2_],
            "df": [df, df_],
            "p-value": [p, p_]
        }, index=["Normal", "Corrected"]
    )
    
    if summary:
        return table
    else:
        return result

def chi_square_fit(data, target, expected, summary=None):
    
    Observed = data[target].value_counts().to_numpy()
    Index = data[target].value_counts().index
    Expected = []
    for var in Index:
        Expected.append(expected[var])
    Expected = np.array(Expected) / np.sum(np.array(Expected)) * np.sum(Observed)
    table = pd.DataFrame(
        {
            "Observed": Observed,
            "Expected": Expected
        }, index = Index
    ).T
    table = table[expected.keys()]
    columns_change = {}
    for columns in table.columns:
        changed = "{}({})".format(target, columns)
        columns_change[columns] = changed
    table = table.rename(columns=columns_change)

    chi2, p = chisquare(Observed, f_exp=Expected)

    result = pd.DataFrame(
        {
            "Chi-Square": chi2,
            "df": Observed.size-1, 
            "p-value": p
        }, index=["Fit"]
    )

    if summary:
        return table
    else:
        return result
"""