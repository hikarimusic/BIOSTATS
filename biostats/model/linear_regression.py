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

    data = data[[x,y]].dropna()
    r = data.corr().iloc[0][1]
    n = len(data)

    summary = pd.DataFrame(
        {
            "Coefficient": r
        }, index=["Correlation"]
    )

    t = r * math.sqrt((n - 2) / (1 - r * r))
    p = CC(lambda: st.t.cdf(t, n-2))
    p = CC(lambda a: 2*min(a, 1-a), p)

    result = pd.DataFrame(
        {
            "D.F." : n-2 ,
            "t Statistic" : t ,
            "p-value" : p
        }, index=["Model"]
    )
    add_p(result)

    process(summary)
    process(result)

    return summary, result

def correlation_matrix(data, variable):

    process(data)

    data = data[variable]

    result = data.corr()

    return result





def simple_linear_regression(data, x, y):

    process(data)

    formula = "Q('%s') ~ " % y
    formula += "Q('%s')" % x
    model = ols(formula, data=data).fit()

    summary = pd.DataFrame(
        {
            "Coefficient" : model.params,
            "Std. Error"  : model.bse,
            "t Statistic" : model.tvalues,
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
            "R-Squared": model.rsquared,
            "Adj. R-Squared": model.rsquared_adj,
            "F Statistic": model.fvalue,
            "p-value": model.f_pvalue
        }, index=["Model"]
    )

    add_p(summary)
    add_p(result)

    process(summary)
    process(result)

    return summary, result



'''
import numpy as np
import pandas as pd

from statsmodels.formula.api import ols
from statsmodels.formula.api import logit
from statsmodels.stats.anova import anova_lm

def linear_regression(data, Y, X, test=None):

    formula = "Q('%s') ~ " % Y
    formula += "Q('%s')" % X
    model = ols(formula, data=data).fit()

    result = pd.read_html(
        model.summary().tables[1].as_html(),header=0,index_col=0
    )[0]
    result = result.drop(columns=['[0.025', '0.975]'])
    result = result.rename(columns={
        'coef' : 'Coefficient',
        'std err' : 'Std. Error',
        't' : 't Statistic',
        'P>|t|' : 'p-value'
    })
    index_change = {}
    for index in result.index:
        changed = index.replace("Q('%s')" % X, X)
        index_change[index] = changed
    result = result.rename(index_change)

    result2 = pd.DataFrame(
        {
            "R-Squared": model.rsquared,
            "Adj. R-Squared": model.rsquared_adj,
            "F Statistic": model.fvalue,
            "p-value": model.f_pvalue
        }, index=["Model"]
    )

    if test:
        return result2
    else:
        return result

def multiple_regression(data, Y, X, X2=[], test=None):

    formula = "Q('%s') ~ " % Y
    for var in X:
        formula += "Q('%s') + " % var
    for var in X2:
        formula += "C(Q('%s')) + " % var
    formula = formula[:-3]
    model = ols(formula, data=data).fit()

    result = pd.read_html(
        model.summary().tables[1].as_html(),header=0,index_col=0
    )[0]
    result = result.drop(columns=['[0.025', '0.975]'])
    result = result.rename(columns={
        'coef' : 'Coefficient',
        'std err' : 'Std. Error',
        't' : 't Statistic',
        'P>|t|' : 'p-value'
    })
    index_change = {}
    for index in result.index:
        changed = index
        for var in X:
            changed = changed.replace("Q('%s')" % var, var)
        for var in X2:
            changed = changed.replace("C(Q('%s'))" % var, var)
            changed = changed.replace('[T.', '(')
            changed = changed.replace(']', ')')
        index_change[index] = changed
    result = result.rename(index_change)

    result2 = pd.DataFrame(
        {
            "R-Squared": model.rsquared,
            "Adj. R-Squared": model.rsquared_adj,
            "F Statistic": model.fvalue,
            "p-value": model.f_pvalue
        }, index=["Model"]
    )

    if test:
        return result2
    else:
        return result

def logistic_regression(data, Y, target, X, X2=[]):
    
    data2 = data[X+X2].copy()
    data2[Y] = 0
    data2.loc[data[Y]==target, Y] = 1

    formula = "Q('%s') ~ " % Y
    for var in X:
        formula += "Q('%s') + " % var
    for var in X2:
        formula += "C(Q('%s')) + " % var
    formula = formula[:-3]
    model = logit(formula, data=data2).fit(disp=0)

    result = pd.read_html(
        model.summary().tables[1].as_html(),header=0,index_col=0
    )[0]
    result = result.drop(columns=['[0.025', '0.975]'])
    result = result.rename(columns={
        'coef' : 'Coefficient',
        'std err' : 'Std. Error',
        'z' : 'z Statistic',
        'P>|z|' : 'p-value'
    })
    index_change = {}
    for index in result.index:
        changed = index
        for var in X:
            changed = changed.replace("Q('%s')" % var, var)
        for var in X2:
            changed = changed.replace("C(Q('%s'))" % var, var)
            changed = changed.replace('[T.', '(')
            changed = changed.replace(']', ')')
        index_change[index] = changed
    result = result.rename(index_change)

    return result
'''