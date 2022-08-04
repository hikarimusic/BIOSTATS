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
    '''
    Test whether there is a correlation between two numeric variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two numeric columns.
    x : :py:class:`str`
        The first numeric variable.
    y : :py:class:`str`
        The second numeric variable. Switching the two variables will not change the result.
    
    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The correlation coefficient and the confidence interval.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, t statistic, and p-value of the test.
    
    See also
    --------
    correlation_matrix : Compute the correlation coefficients between every two variables.
    simple_linear_regression : Fit an equation that predicts a numeric variable from another numeric variable.
    spearman_rank_correlation : The non-parametric version of correlation test.
    
    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("correlation.csv")
    >>> data
        Latitude  Species
    0     39.217    128.0
    1     38.800    137.0
    2     39.467    108.0
    3     38.958    118.0
    4     38.600    135.0
    5     38.583     94.0
    6     39.733    113.0
    7     38.033    118.0
    8     38.900     96.0
    9     39.533     98.0
    10    39.133    121.0
    11    38.317    152.0
    12    38.333    108.0
    13    38.367    118.0
    14    37.200    157.0
    15    37.967    125.0
    16    37.667    114.0

    We want to test whether there is a correlation between *Latitude* and *Species*.

    >>> summary, result = bs.correlation(data=data, x="Latitude", y="Species")
    >>> summary
                 Coefficient  95% CI: Lower  95% CI: Upper
    Correlation    -0.462884      -0.771814       0.022842

    The correlation coefficient and the confidence interval are given.

    >>> result
           D.F.  t Statistic   p-value    
    Model  15.0    -2.022457  0.061336 NaN

    The p-value > 0.05, so there is no significant correlation between *Latitude* and *Species*.

    '''

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
    '''
    Compute the correlation coefficients between every two variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two numeric columns.
    variable : :py:class:`list`
        The list of numeric variables.
    
    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The correlation matrix.
    
    See also
    --------
    correlation : Test whether there is a correlation between two numeric variables.
    multiple_linear_regression : Fit an equation that predicts a numeric variable from other variables.
    
    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("correlation_matrix.csv")
    >>> data
        Longnose  Acerage   DO2  Maxdepth   NO3    SO4  Temp
    0       13.0   2528.0   9.6      80.0  2.28  16.75  15.3
    1       12.0   3333.0   8.5      83.0  5.34   7.74  19.4
    2       54.0  19611.0   8.3      96.0  0.99  10.92  19.5
    3       19.0   3570.0   9.2      56.0  5.44  16.53  17.0
    4       37.0   1722.0   8.1      43.0  5.66   5.91  19.3
    ..       ...      ...   ...       ...   ...    ...   ...
    63       2.0   6311.0   7.6      46.0  0.64  21.16  18.5
    64      26.0   1450.0   7.9      60.0  2.96   8.84  18.6
    65      20.0   4106.0  10.0      96.0  2.62   5.45  15.4
    66      38.0  10274.0   9.3      90.0  5.45  24.76  15.0
    67      19.0    510.0   6.7      82.0  5.25  14.19  26.5

    We want to compute the correlation coefficients between every two variables in the data.

    >>> summary = bs.correlation_matrix(data=data, variable=["Longnose","Acerage","DO2","Maxdepth","NO3","SO4","Temp"])
    >>> summary
              Longnose   Acerage      Temp  Maxdepth       DO2       SO4       NO3
    Longnose  1.000000  0.346506  0.139865  0.304980  0.136157 -0.017380  0.309233
    Acerage   0.346506  1.000000  0.003541  0.258624 -0.022433  0.048776 -0.099528
    Temp      0.139865  0.003541  1.000000 -0.004895 -0.318865  0.079792 -0.001596
    Maxdepth  0.304980  0.258624 -0.004895  1.000000 -0.057570 -0.049872  0.036269
    DO2       0.136157 -0.022433 -0.318865 -0.057570  1.000000 -0.072411  0.273426
    SO4      -0.017380  0.048776  0.079792 -0.049872 -0.072411  1.000000 -0.087130
    NO3       0.309233 -0.099528 -0.001596  0.036269  0.273426 -0.087130  1.000000

    The correlation matrix is computed.

    '''

    process(data)
    data = data[list(set(variable))].dropna()

    for var in variable:
        if str(data[var].dtypes) != "float64":
            raise Warning("The column '{}' must be numeric".format(var))

    result = data.corr()

    return result


def simple_linear_regression(data, x, y):
    '''
    Fit an equation that predicts a numeric variable from another numeric variable.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two numeric columns.
    x : :py:class:`str`
        The predictor variable. Must be numeric.
    y : :py:class:`str`
        The response variable. Must be numeric.
    
    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The coefficients of the fitted equation, along with the confidence intervals, standard errors, t statistics, and p-values.
    result : :py:class:`pandas.DataFrame`
        The R-squared, adjusted R-squared, F statistic, and p-value of the fitted model.
    
    See also
    --------
    multiple_linear_regression : Fit an equation that predicts a numeric variable from other variables.
    simple_logistic_regression : Fit an equation that predicts a dichotomous categorical variable from a numeric variable.
    correlation : Test the correlation between two numeric variables.
    
    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("simple_linear_regression.csv")
    >>> data
        Weight  Eggs
    0     5.38  29.0
    1     7.36  23.0
    2     6.13  22.0
    3     4.75  20.0
    4     8.10  25.0
    5     8.62  25.0
    6     6.30  17.0
    7     7.44  24.0
    8     7.26  20.0
    9     7.17  27.0
    10    7.78  24.0
    11    6.23  21.0
    12    5.42  22.0
    13    7.87  22.0
    14    5.25  23.0
    15    7.37  35.0
    16    8.01  27.0
    17    4.92  23.0
    18    7.03  25.0
    19    6.45  24.0
    20    5.06  19.0
    21    6.72  21.0
    22    7.00  20.0
    23    9.39  33.0
    24    6.49  17.0
    25    6.34  21.0
    26    6.16  25.0
    27    5.74  22.0

    We want to fit an equation that predicts *Eggs* from *Weight*.

    >>> summary, result = bs.simple_linear_regression(data=data, x="Weight", y="Eggs")
    >>> summary
               Coefficient  95% CI: Lower  95% CI: Upper  Std. Error  t Statistic   p-value    
    Intercept    12.689022       4.054035      21.324009    4.200858     3.020579  0.005598  **
    Weight        1.601722       0.332202       2.871243    0.617612     2.593411  0.015401   *

    The coefficients of the fitted equation, along with confidence intervals and p-values are given.

    >>> result
           R-Squared  Adj. R-Squared  F Statistic   p-value   
    Model   0.205519        0.174962      6.72578  0.015401  *

    The p-value < 0.05, so there is a significant relation between the predictor and response variables.
    
    '''

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
    Fit an equation that predicts a numeric variable from other variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and several other columns (can be either numeric or categorical).
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
        The R-squared, adjusted R-squared, F statistic, and p-value of the fitted model.
    
    See also
    --------
    multiple_logistic_regression : Fit an equation that predicts a categorical variable from other variables.
    correlation_matrix : Compute the correlation coefficients between every two variables.

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

    We want to fit an equation that predicts *Longnose* from *Acerage*, *Maxdepth*, and *NO3*.

    >>> summary, result = bs.multiple_linear_regression(data=data, x_numeric=["Acerage", "Maxdepth", "NO3"], x_categorical=[], y="Longnose")
    >>> summary
               Coefficient  95% CI: Lower  95% CI: Upper  Std. Error  t Statistic   p-value     
    Intercept   -23.829067     -54.342374       6.684240   15.273992    -1.560107  0.123666  NaN
    Acerage       0.001988       0.000641       0.003334    0.000674     2.947947  0.004461   **
    Maxdepth      0.336605      -0.018134       0.691344    0.177571     1.895610  0.062529  NaN
    NO3           8.673044       3.132716      14.213372    2.773312     3.127323  0.002654   **

    The coefficients of the fitted equation, along with confidence intervals and p-values are given.

    >>> result
           R-Squared  Adj. R-Squared  F Statistic   p-value     
    Model   0.279826        0.246068     8.289157  0.000097  ***

    The p-value < 0.001, so there is a significant relation between the predictor and response variables.
    
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
