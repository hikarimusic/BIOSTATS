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
    data = data[list({variable_1, variable_2})].dropna()

    if data[variable_1].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_1))
    if data[variable_2].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_2))

    summary = pd.crosstab(index=data[variable_1], columns=data[variable_2])
    summary.index.name = None
    summary.columns.name = None

    obs = summary.values.tolist()

    rr = CC(lambda: len(obs))
    cc = CC(lambda: len(obs[0]))
    r_sum = []
    c_sum = []
    _sum = 0

    for i in range(rr):
        temp = 0
        for j in range(cc):
            temp = CC(lambda: temp + obs[i][j])
        r_sum.append(temp)
    for j in range(cc):
        temp = 0
        for i in range(rr):
            temp = CC(lambda: temp + obs[i][j])
        c_sum.append(temp)
    for i in range(rr):
        _sum = CC(lambda: _sum + r_sum[i])
    
    exp = []

    for i in range(rr):
        temp = []
        for j in range(cc):
            temp.append(CC(lambda: r_sum[i] * c_sum[j] / _sum))
        exp.append(temp)
    
    chi2 = 0
    for i in range(rr):
        for j in range(cc):
            chi2 = CC(lambda: chi2 + (obs[i][j]-exp[i][j]) ** 2 / exp[i][j])
    
    p = CC(lambda: 1 - st.chi2.cdf(chi2, (rr-1)*(cc-1)))

    result = pd.DataFrame(
        {
            "D.F.": CC(lambda: (rr-1)*(cc-1)),
            "Chi Square": CC(lambda: chi2),
            "p-value": CC(lambda: p)
        }, index=["Normal"]
    )

    if summary.shape == (2,2):
        chi2 = 0
        for i in range(rr):
            for j in range(cc):
                chi2 = CC(lambda: chi2 + (abs(obs[i][j]-exp[i][j])-0.5) ** 2 / exp[i][j])
        
        p = CC(lambda: 1 - st.chi2.cdf(chi2, (rr-1)*(cc-1)))

        result2 = pd.DataFrame(
            {
            "D.F.": CC(lambda: (rr-1)*(cc-1)),
            "Chi Square": CC(lambda: chi2),
            "p-value": CC(lambda: p)
            }, index=["Corrected"]
        )
        result = pd.concat([result, result2], axis=0)
    
    add_p(result)

    process(summary)
    process(result)

    return summary, result

def chi_square_test_fit(data, variable, expect):
    
    process(data)
    data = data[[variable]].dropna()

    if data[variable].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable))

    cat = data.groupby(variable, sort=False)[variable].groups.keys()
    obs = []
    exp = []
    for var in cat:
        obs.append(CC(lambda: data[variable].value_counts()[var]))
    exp_val = list(expect.values())
    for var in cat:
        exp.append(CC(lambda: expect[var] * sum(obs) / sum(exp_val)))
    dim = CC(lambda: len(obs))

    summary = pd.DataFrame(
        {
            "Observe" : CC(lambda: obs),
            "Expect"  : CC(lambda: exp)
        }, index=cat
    )

    chi2 = 0
    for i in range(dim):
        chi2 = CC(lambda: chi2 + (obs[i]-exp[i]) * (obs[i]-exp[i]) / exp[i])
    p = CC(lambda: 1 - st.chi2.cdf(chi2, dim-1))
    result = pd.DataFrame(
        {
            "D.F.": CC(lambda: dim-1),
            "Chi Square": CC(lambda: chi2),
            "p-value": CC(lambda: p)
        }, index=["Normal"]
    )

    add_p(result)

    process(summary)
    process(result)

    return summary, result

def mcnemar_test(data, variable_1, variable_2, pair):

    process(data)
    data = data[list({variable_1, variable_2, pair})].dropna()

    if data[variable_1].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_1))
    if data[variable_2].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_2))
    if data[pair].nunique() > 2000:
        raise Warning("The nmuber of classes in column '{}' cannot > 2000.".format(pair))

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

    chi2 = CC(lambda: (b - c) ** 2 / (b + c))
    chi2_ = CC(lambda: (abs(b-c) - 1) ** 2 / (b + c))
    p = CC(lambda: 1 - st.chi2.cdf(chi2, 1))
    p_ = CC(lambda: 1 - st.chi2.cdf(chi2_, 1))

    result = pd.DataFrame(
        {
            "D.F." : [1, 1] ,
            "Chi Square" : [chi2, chi2_] ,
            "p-value" : [p, p_]
        }, index=["Normal", "Corrected"]
    )
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def mantel_haenszel_test(data, variable_1, variable_2, stratum):
    
    process(data)
    data = data[list({variable_1, variable_2, stratum})].dropna()

    if data[variable_1].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_1))
    if data[variable_2].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_2))
    if data[stratum].nunique() > 30:
        raise Warning("The nmuber of classes in column '{}' cannot > 30.".format(stratum))

    study = data[stratum].dropna().unique()
    grp_1 = data[variable_1].value_counts()[:2].index.tolist()
    grp_2 = data[variable_2].value_counts()[:2].index.tolist()

    summary = pd.DataFrame(columns=["", grp_2[0], grp_2[1]])

    O, V, E = 0, 0 ,0

    for stu in study:
        part = data.loc[data[stratum]==stu]
        a = CC(lambda: part[(part[variable_1]==grp_1[0]) & (part[variable_2]==grp_2[0])][stratum].count())
        b = CC(lambda: part[(part[variable_1]==grp_1[0]) & (part[variable_2]==grp_2[1])][stratum].count())
        c = CC(lambda: part[(part[variable_1]==grp_1[1]) & (part[variable_2]==grp_2[0])][stratum].count())
        d = CC(lambda: part[(part[variable_1]==grp_1[1]) & (part[variable_2]==grp_2[1])][stratum].count())
        n = CC(lambda: a + b + c + d)
        temp = pd.DataFrame(
            {
                "" : [grp_1[0], grp_1[1], ""] ,
                grp_2[0] : [a, c, np.nan] ,
                grp_2[1] : [b, d, np.nan]
            }, index=[stu, "", ""]
        )
        summary = pd.concat([summary, temp])

        O = CC(lambda: O + a)
        E = CC(lambda: E + (a + b) * (a + c) / n)
        V = CC(lambda: V + (a + b) * (c + d) * (a + c) * (b + d) / (n**3 - n**2))
    
    chi2 = CC(lambda: (abs(O-E) - 0.5) ** 2 / V)
    p = CC(lambda: 1 - st.chi2.cdf(chi2, 1))

    result = pd.DataFrame(
        {
            "D.F.": 1,
            "Chi Square": CC(lambda: chi2),
            "p-value": CC(lambda: p)
        }, index=["Normal"]
    )
    add_p(result)

    process(summary)
    process(result)

    return summary, result
