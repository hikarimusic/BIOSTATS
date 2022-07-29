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

def multiple_linear_regression(data, x_numeric, x_categorical, y):
    '''
    Fit an equation that can predict a numeric variable from other variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must Contain at least one numeric column and several other variables (can be either numeric or categorical).
    x_numeric : :py:class:`list`
        The list of predictor variables that are numeric.
    x_categorical : :py:class:`list`
        The list of predictor variables that are categorical.
    y : :py:class:`str`
        The response variable. Must be numeric.
    
    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The coefficients of the fitted equation, along with the confidence intervals, standard errors, t statistics, and p-values.
    result : :py:class:`pandas.DataFrame`
        The R-squared, adjusted R-squared, F statistic, and p-value of the fitting model.
    
    See also
    --------
    simple_linear_regression : Fit an equation that can predict a numeric variable from another numeric variables.
    multinomial_logistic_regression : Fit an equation that can predict a categorical variable from other variables.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("multiple_linear_regression.csv")
    >>> data
        Acerage  Maxdepth   NO3  Longnose
    0    2528.0      80.0  2.28      13.0
    1    3333.0      83.0  5.34      12.0
    2   19611.0      96.0  0.99      54.0
    3    3570.0      56.0  5.44      19.0
    4    1722.0      43.0  5.66      37.0
    ..      ...       ...   ...       ...
    63   6311.0      46.0  0.64       2.0
    64   1450.0      60.0  2.96      26.0
    65   4106.0      96.0  2.62      20.0
    66  10274.0      90.0  5.45      38.0
    67    510.0      82.0  5.25      19.0

    We want to fit an equation to predict *Longnose* from *Acerage*, *Maxdepth*, and *NO3*.

    >>> summary, result = bs.multiple_linear_regression(data=data, x_numeric=["Acerage", "Maxdepth", "NO3"], x_categorical=[], y="Longnose")
    >>> summary
               Coefficient  95% CI: Lower  95% CI: Upper  Std. Error  t Statistic   p-value     
    Intercept   -23.829067     -54.342374       6.684240   15.273992    -1.560107  0.123666  NaN
    Acerage       0.001988       0.000641       0.003334    0.000674     2.947947  0.004461   **
    Maxdepth      0.336605      -0.018134       0.691344    0.177571     1.895610  0.062529  NaN
    NO3           8.673044       3.132716      14.213372    2.773312     3.127323  0.002654   **

    The coefficients of the fitted equation, along with confidence intervals and p-values.

    >>> result
           R-Squared  Adj. R-Squared  F Statistic   p-value     
    Model   0.279826        0.246068     8.289157  0.000097  ***

    The p-value < 0.001, which means there is a significant relation between the predictor and response variables. The R-Squared < 0.3, which indicates the equation did not fit the data very well.
    
    '''

    process(data)
    data = data[list(set(x_numeric+x_categorical+[y]))].dropna()

    for var in x_numeric:
        if str(data[var].dtypes) != "float64":
            raise Warning("The column '{}' must be numeric".format(var))
    for var in x_categorical:
        if data[var].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(var))
    if str(data[y].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(y))

    formula = "Q('%s') ~ " % y
    for var in x_numeric:
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
        for var in x_numeric:
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
