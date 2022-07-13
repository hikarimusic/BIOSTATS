import numpy as np
import pandas as pd

from statsmodels.formula.api import logit

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


def simple_logistic_regression(data, x, y, target):
    
    process(data)

    data2 = data[[x]].copy()
    data2[y] = 0
    data2.loc[data[y]==target, y] = 1

    formula = "Q('%s') ~ " % y
    formula += "Q('%s')" % x
    model = logit(formula, data=data2).fit(disp=0)
    
    summary = pd.DataFrame(
        {
            "Coefficient" : model.params,
            "Std. Error"  : model.bse,
            "z Statistic" : model.tvalues,
            "p-value"     : model.pvalues
        }
    )
    index_change = {}
    for index in summary.index:
        changed = index.replace("Q('%s')" % x, x)
        index_change[index] = changed
    summary = summary.rename(index_change)

    result = pd.DataFrame(
        {
            "Pseudo R-Squared": model.prsquared,
            "p-value": model.llr_pvalue
        }, index=["Model"]
    )

    add_p(summary)
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def multiple_logistic_regression(data, x_nominal, x_categorical, y, target):
    
    process(data)

    data2 = data[x_nominal+x_categorical].copy()
    data2[y] = 0
    data2.loc[data[y]==target, y] = 1

    formula = "Q('%s') ~ " % y
    for var in x_nominal:
        formula += "Q('%s') + " % var
    for var in x_categorical:
        formula += "C(Q('%s')) + " % var
    formula = formula[:-3]
    model = logit(formula, data=data2).fit(disp=0)
    
    summary = pd.DataFrame(
        {
            "Coefficient" : model.params,
            "Std. Error"  : model.bse,
            "z Statistic" : model.tvalues,
            "p-value"     : model.pvalues
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
            "Pseudo R-Squared": model.prsquared,
            "p-value": model.llr_pvalue
        }, index=["Model"]
    )

    add_p(summary)
    add_p(result)

    process(summary)
    process(result)

    return summary, result
