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

def chi_square_test(data, variable_1, variable_2, kind="count"):
    '''
    Test whether there is an association between two categorical variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must Contain at least two categorical columns.
    variable_1 : :py:class:`str`
        The name of the first categorical column.
    variable_2 : :py:class:`str`
        The name of the second categorical column. Switching the two variables will not change the result of chi-square test.
    kind : :py:class:`str`
        The way to summarize the contingency table.
        * "count" : Count the appearance.
        * "vertical" : Calculate the proportion vertically, so that the sum of each column equals 1.
        * "horizontal" : Calculate the proportion horizontally, so that the sum of each row equals 1.
        * "overall" : Calculate the overall proportion, so that the sum of the whole table equals 1.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The contingency table of the two categorical columns.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, t statistic, and p-value of the test.

    See also
    --------
    fisher_exact_test : The exact version of chi-square test.
    mantel_haenszel_test : Test the association between two categorical variables in stratified data.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("chi_square_test.csv")
    >>> data
         Genotype      Health
    0     ins-del     disease
    1     ins-ins     disease
    2     ins-del     disease
    3     ins-ins     disease
    4     ins-del  no_disease
    ...       ...         ...
    2254  ins-ins  no_disease
    2255  ins-del     disease
    2256  ins-del     disease
    2257  ins-ins     disease
    2258  ins-ins  no_disease

    We want to test whether there is an association between *Genotype* and *Health*.

    >>> summary, result = bs.chi_square_test(data=data, variable_1="Genotype", variable_2="Health", kind="horizontal")
    >>> summary
              disease  no_disease
    del-del  0.814159    0.185841
    ins-del  0.792276    0.207724
    ins-ins  0.750698    0.249302

    The proportion of *disease* in different *Genotype*.

    >>> result
            D.F.  Chi Square   p-value   
    Normal   2.0    7.259386  0.026524  *

    The p-value < 0.05, so there is a significant association between *Genotype* and *Health*. That is, the proportions of *disease* are different between the three *Genotype*.

    '''
    
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

    if kind == "vertical":
        col_sum = CC(lambda: summary.sum(axis=0))
        for i in range(summary.shape[0]):
            for j in range(summary.shape[1]):
                summary.iat[i,j] = CC(lambda: summary.iat[i,j] / col_sum[j])

    if kind == "horizontal":
        col_sum = CC(lambda: summary.sum(axis=1))
        for i in range(summary.shape[0]):
            for j in range(summary.shape[1]):
                summary.iat[i,j] = CC(lambda: summary.iat[i,j] / col_sum[i])

    if kind == "overall":
        _sum = CC(lambda: summary.to_numpy().sum())
        for i in range(summary.shape[0]):
            for j in range(summary.shape[1]):
                summary.iat[i,j] = CC(lambda: summary.iat[i,j] / _sum)

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
