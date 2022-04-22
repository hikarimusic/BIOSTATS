import numpy as np
import pandas as pd

from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

def linear_regression(data=None, Y=None, X=None, test=None):

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

    if test == 1:
        return result2
    else:
        return result

def multiple_regression(data=None, Y=None, X=None, test=None):

    formula = "Q('%s') ~ " % Y
    for var in X:
        formula += "Q('%s') + " % var
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

    if test == 1:
        return result2
    else:
        return result
