import numpy as np
import pandas as pd
from scipy import stats as st
import math

from statsmodels.formula.api import ols

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

def correlation(data, x, y):

    process(data)   
    data = data[list({x, y})].dropna()

    if str(data[x].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(x))
    if str(data[y].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(y))

    n = CC(lambda: len(data))
    r, p = CC(lambda: st.pearsonr(data[x], data[y]))
    r_z = CC(lambda: np.arctanh(r))
    rz_l = CC(lambda: st.norm.ppf(0.025, r_z, 1/np.sqrt(n-3)))
    rz_h = CC(lambda: st.norm.ppf(0.975, r_z, 1/np.sqrt(n-3)))
    r_l = CC(lambda: np.tanh(rz_l))
    r_h = CC(lambda: np.tanh(rz_h))

    summary = pd.DataFrame(
        {
            "Coefficient": CC(lambda: r) ,
            "95% CI: Lower": CC(lambda: r_l), 
            "95% CI: Upper": CC(lambda: r_h)
        }, index=["Correlation"]
    )

    t = CC(lambda: r * math.sqrt((n - 2) / (1 - r * r)))
    p = CC(lambda: st.t.cdf(t, n-2))
    p = CC(lambda: 2*min(p, 1-p))

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

def correlation_matrix(data, variable):

    process(data)
    data = data[list(set(variable))].dropna()

    for var in variable:
        if str(data[var].dtypes) != "float64":
            raise Warning("The column '{}' must be numeric".format(var))

    result = data.corr()

    return result


def simple_linear_regression(data, x, y):

    process(data)
    data = data[list({x, y})].dropna()

    if str(data[x].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(x))
    if str(data[y].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(y))


    formula = "Q('%s') ~ " % y
    formula += "Q('%s')" % x
    model = ols(formula, data=data).fit()

    summary = pd.DataFrame(
        {
            "Coefficient"   : CC(lambda: model.params),
            "95% CI: Lower" : CC(lambda: model.conf_int()[0]) ,
            "95% CI: Upper" : CC(lambda: model.conf_int()[1]) ,
            "Std. Error"    : CC(lambda: model.bse),
            "t Statistic"   : CC(lambda: model.tvalues),
            "p-value"       : CC(lambda: model.pvalues)
        }
    )
    index_change = {}
    for index in summary.index:
        changed = index.replace("Q('%s')" % x, x)
        index_change[index] = changed
    summary = summary.rename(index_change)

    result = pd.DataFrame(
        {
            "R-Squared": CC(lambda: model.rsquared),
            "Adj. R-Squared": CC(lambda: model.rsquared_adj),
            "F Statistic": CC(lambda: model.fvalue),
            "p-value": CC(lambda: model.f_pvalue)
        }, index=["Model"]
    )

    add_p(summary)
    add_p(result)

    process(summary)
    process(result)

    return summary, result

def multiple_linear_regression(data, x_nominal, x_categorical, y):

    process(data)
    data = data[list(set(x_nominal+x_categorical+[y]))].dropna()

    for var in x_nominal:
        if str(data[var].dtypes) != "float64":
            raise Warning("The column '{}' must be numeric".format(var))
    for var in x_categorical:
        if data[var].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(var))
    if str(data[y].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(y))

    formula = "Q('%s') ~ " % y
    for var in x_nominal:
        formula += "Q('%s') + " % var
    for var in x_categorical:
        formula += "C(Q('%s')) + " % var
    formula = formula[:-3]
    model = ols(formula, data=data).fit()

    summary = pd.DataFrame(
        {
            "Coefficient"   : CC(lambda: model.params),
            "95% CI: Lower" : CC(lambda: model.conf_int()[0]) ,
            "95% CI: Upper" : CC(lambda: model.conf_int()[1]) ,
            "Std. Error"    : CC(lambda: model.bse),
            "t Statistic"   : CC(lambda: model.tvalues),
            "p-value"       : CC(lambda: model.pvalues)
        }
    )
    index_change = {}
    for index in summary.index:
        changed = index
        for var in x_nominal:
            changed = changed.replace("Q('%s')" % var, var)
        for var in x_categorical:
            changed = changed.replace("C(Q('%s'))" % var, var)
            changed = changed.replace('[T.', ' (')
            changed = changed.replace(']', ')')
        index_change[index] = changed
    summary = summary.rename(index_change)

    result = pd.DataFrame(
        {
            "R-Squared": CC(lambda: model.rsquared),
            "Adj. R-Squared": CC(lambda: model.rsquared_adj),
            "F Statistic": CC(lambda: model.fvalue),
            "p-value": CC(lambda: model.f_pvalue)
        }, index=["Model"]
    )

    add_p(summary)
    add_p(result)

    process(summary)
    process(result)

    return summary, result
