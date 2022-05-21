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
        'P>\vert t\vert ' : 'p-value'
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
        'P>\vert t\vert ' : 'p-value'
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
        'P>\vert z\vert ' : 'p-value'
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
