import numpy as np
import pandas as pd

from statsmodels.formula.api import logit
from statsmodels.miscmodels.ordinal_model import OrderedModel
from statsmodels.discrete.discrete_model import MNLogit

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
    '''
    Fit an equation that predicts a dichotomous categorical variable from a numeric variable.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one categorical column and one numeric column.
    x : :py:class:`str`
        The predictor variable. Must be numeric.
    y : :py:class:`str`
        The response variable. Must be categorical.
    target : :py:class:`str` or :py:class:`int` or :py:class:`float`
        The target group of the categorical variable.
    
    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The coefficients of the fitted equation, along with the confidence intervals, standard errors, z statistics, and p-values.
    result : :py:class:`pandas.DataFrame`
        The pseudo R-squared and p-value of the fitted model.
    
    See also
    --------
    multiple_logistic_regression : Fit an equation that predicts a dichotomous categorical variable from other variables.
    ordered_logistic_regression : Fit an equation that predicts an ordered categorical variable from other variables.
    multinomial_logistic_regression : Fit an equation that predicts a multinomial categorical variable from other variables.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("simple_logistic_regression.csv")
    >>> data
        Continuous Factor
    0         62.0      A
    1         63.0      A
    2         64.0      A
    3         65.0      A
    4         66.0      A
    5         67.0      A
    6         68.0      A
    7         69.0      A
    8         70.0      A
    9         71.0      A
    10        72.0      A
    11        73.0      A
    12        74.0      A
    13        75.0      A
    14        72.5      B
    15        73.5      B
    16        74.5      B
    17        75.0      B
    18        76.0      B
    19        77.0      B
    20        78.0      B
    21        79.0      B
    22        80.0      B
    23        81.0      B
    24        82.0      B
    25        83.0      B
    26        84.0      B
    27        85.0      B
    28        86.0      B

    We want to fit an equation that predicts *Factor* from *Continuous*.

    >>> summary, result = bs.simple_logistic_regression(data=data, x="Continuous", y="Factor", target="B")
    >>> summary
                Coefficient  95% CI: Lower  95% CI: Upper  Std. Error  z Statistic   p-value   
    Intercept    -66.498134    -129.959199      -3.037069   32.378689    -2.053762  0.039999  *
    Continuous     0.902667       0.042352       1.762982    0.438945     2.056449  0.039739  *

    The coefficients of the fitted equation, along with confidence intervals and p-values are given.

    >>> result
           Pseudo R-Squared       p-value     
    Model          0.697579  1.200433e-07  ***

    The p-value < 0.001, so there is a significant relation between the predictor and response variables.

    '''

    process(data)
    data = data[list({x, y})].dropna()

    if str(data[x].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(x))
    if data[y].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(y))

    data2 = data[[x]].copy()
    data2[y] = 0
    data2.loc[data[y]==target, y] = 1

    formula = "Q('%s') ~ " % y
    formula += "Q('%s')" % x
    model = logit(formula, data=data2).fit(disp=0)
    
    summary = pd.DataFrame(
        {
            "Coefficient"   : CC(lambda: model.params),
            "95% CI: Lower" : CC(lambda: model.conf_int()[0]) ,
            "95% CI: Upper" : CC(lambda: model.conf_int()[1]) ,
            "Std. Error"    : CC(lambda: model.bse),
            "z Statistic"   : CC(lambda: model.tvalues),
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
            "Pseudo R-Squared": CC(lambda: model.prsquared),
            "p-value": CC(lambda: model.llr_pvalue)
        }, index=["Model"]
    )

    add_p(summary)
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def multiple_logistic_regression(data, x_numeric, x_categorical, y, target):
    '''
    Fit an equation that predicts a dichotomous categorical variable from other variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one categorical column and several other columns (can be either numeric or categorical).
    x_numeric : :py:class:`list`
        The list of predictor variables that are numeric.
    x_categorical : :py:class:`list`
        The list of predictor variables that are categorical.
    y : :py:class:`str`
        The response variable. Must be categorical.
    target : :py:class:`str` or :py:class:`int` or :py:class:`float`
        The target group of the categorical variable.
    
    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The coefficients of the fitted equation, along with the confidence intervals, standard errors, z statistics, and p-values.
    result : :py:class:`pandas.DataFrame`
        The pseudo R-squared and p-value of the fitted model.
    
    See also
    --------
    ordered_logistic_regression : Fit an equation that predicts an ordered categorical variable from other variables.
    multinomial_logistic_regression : Fit an equation that predicts a multinomial categorical variable from other variables.
    multiple_linear_regression : Fit an equation that predicts a numeric variable from other variables.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("multiple_logistic_regression.csv")
    >>> data
        Upland  Migr    Mass  Indiv  Insect  Wood  Status
    0      0.0   1.0  9600.0   29.0    12.0   0.0     1.0
    1      0.0   1.0  5000.0   85.0     0.0   0.0     1.0
    2      0.0   1.0  3360.0    8.0     0.0   0.0     1.0
    3      0.0   3.0  2517.0   10.0    12.0   0.0     0.0
    4      0.0   3.0  3170.0    7.0     0.0   0.0     0.0
    ..     ...   ...     ...    ...     ...   ...     ...
    74     0.0   1.0    23.6   29.0    12.0   1.0     1.0
    75     0.0   1.0    20.7    9.0    12.0   0.0     0.0
    76     0.0   3.0    31.0    2.0    12.0   1.0     0.0
    77     0.0   2.0    36.9    2.0     8.0   0.0     0.0
    78     0.0   2.0   106.5    2.0    12.0   0.0     0.0

    We want to fit an equation that predicts *Status* from *Upland*, *Migr*, *Mass*, *Indiv*, *Insect*, and *Wood*.

    >>> summary, result = bs.multiple_logistic_regression(data=data, x_numeric=["Upland", "Migr", "Mass", "Indiv", "Insect", "Wood"], x_categorical=[], y="Status", target="1")
    >>> summary
               Coefficient  95% CI: Lower  95% CI: Upper  Std. Error  z Statistic   p-value     
    Intercept    -3.549648      -7.631768       0.532472    2.082753    -1.704306  0.088324  NaN
    Upland       -4.548429      -8.608058      -0.488800    2.071277    -2.195954  0.028095    *
    Migr         -1.818405      -3.450219      -0.186591    0.832573    -2.184077  0.028957    *
    Mass          0.001903       0.000521       0.003284    0.000705     2.699675  0.006941   **
    Indiv         0.013706       0.006120       0.021292    0.003870     3.541316  0.000398  ***
    Insect        0.239472      -0.029721       0.508666    0.137346     1.743566  0.081235  NaN
    Wood          1.813444      -0.755285       4.382174    1.310601     1.383674  0.166458  NaN

    The coefficients of the fitted equation, along with confidence intervals and p-values are given.

    >>> result
           Pseudo R-Squared       p-value     
    Model           0.67443  1.125372e-11  ***

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
    if data[y].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(y))

    try:
        target = float(target)
    except:
        pass

    data2 = data[x_numeric+x_categorical].copy()
    data2[y] = 0
    data2.loc[data[y]==target, y] = 1

    formula = "Q('%s') ~ " % y
    for var in x_numeric:
        formula += "Q('%s') + " % var
    for var in x_categorical:
        formula += "C(Q('%s')) + " % var
    formula = formula[:-3]
    model = logit(formula, data=data2).fit(disp=0)
    
    summary = pd.DataFrame(
        {
            "Coefficient"   : CC(lambda: model.params),
            "95% CI: Lower" : CC(lambda: model.conf_int()[0]) ,
            "95% CI: Upper" : CC(lambda: model.conf_int()[1]) ,
            "Std. Error"    : CC(lambda: model.bse),
            "z Statistic"   : CC(lambda: model.tvalues),
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
            "Pseudo R-Squared": CC(lambda: model.prsquared),
            "p-value": CC(lambda: model.llr_pvalue)
        }, index=["Model"]
    )

    add_p(summary)
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def ordered_logistic_regression(data, x_numeric, x_categorical, y, order):
    '''
    Fit an equation that predicts an ordered categorical variable from other variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one categorical column and several other columns (can be either numeric or categorical).
    x_numeric : :py:class:`list`
        The list of predictor variables that are numeric.
    x_categorical : :py:class:`list`
        The list of predictor variables that are categorical.
    y : :py:class:`str`
        The response variable. Must be categorical.
    order : :py:class:`dict`
        The order of groups in the categorical variable.
    
    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The coefficients of the fitted equation, along with the confidence intervals, standard errors, z statistics, and p-values.
    result : :py:class:`pandas.DataFrame`
        The pseudo R-squared and p-value of the fitted model.
    
    See also
    --------
    multiple_logistic_regression : Fit an equation that predicts a dichotomous categorical variable from other variables.
    multinomial_logistic_regression : Fit an equation that predicts a multinomial categorical variable from other variables.
    multiple_linear_regression : Fit an equation that predicts a numeric variable from other variables.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("ordered_logistic_regression.csv")
    >>> data
         pared  public   gpa            apply
    0      0.0     0.0  3.26      very likely
    1      1.0     0.0  3.21  somewhat likely
    2      1.0     1.0  3.94         unlikely
    3      0.0     0.0  2.81  somewhat likely
    4      0.0     0.0  2.53  somewhat likely
    ..     ...     ...   ...              ...
    395    0.0     0.0  3.70         unlikely
    396    0.0     0.0  2.63         unlikely
    397    0.0     0.0  2.25  somewhat likely
    398    0.0     0.0  3.26  somewhat likely
    399    0.0     0.0  3.52      very likely

    We want to fit an equation that predicts *apply* from *pared*, *public*, and *gpa*.

    >>> summary, result = bs.ordered_logistic_regression(data=data, x_numeric=["pared", "public", "gpa"], x_categorical=[], y="apply", 
    ...     order={"unlikely":1, "somewhat likely":2, "very likely":3})
    >>> summary
                                   Coefficient  95% CI: Lower  95% CI: Upper  Std. Error  z Statistic   p-value     
    pared                             1.047678       0.526740       1.568616    0.265789     3.941761  0.000081  ***
    public                           -0.058675      -0.642471       0.525121    0.297861    -0.196987  0.843838  NaN
    gpa                               0.615740       0.104912       1.126568    0.260631     2.362495  0.018152    *
    unlikely / somewhat likely        2.203303       0.675441       3.731164         NaN          NaN       NaN  NaN
    somewhat likely / very likely     4.298752       2.466471       6.182776         NaN          NaN       NaN  NaN

    The coefficients of the fitted equation, along with confidence intervals and p-values are given.

    >>> result
           Pseudo R-Squared       p-value     
    Model           0.67443  1.125372e-11  ***

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
    if data[y].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(y))

    data[y] = data[y].astype(pd.CategoricalDtype(categories=[x[0] for x in sorted(order.items(), key=lambda item: item[1])], ordered=True))
    n = len(order)

    formula = "%s ~ " % y
    for var in x_numeric:
        formula += "%s + " % var
    for var in x_categorical:
        formula += "C(%s) + " % var
    formula = formula[:-3]

    model_0 = OrderedModel.from_formula(formula, data=data, distr="logit")
    model = model_0.fit(disp=False)

    summary = pd.DataFrame(
        {
            "Coefficient"   : CC(lambda: model.params),
            "95% CI: Lower" : CC(lambda: model.conf_int()[0]) ,
            "95% CI: Upper" : CC(lambda: model.conf_int()[1]) ,
            "Std. Error"    : CC(lambda: model.bse),
            "z Statistic"   : CC(lambda: model.tvalues),
            "p-value"       : CC(lambda: model.pvalues)
        }
    )
    summary.iloc[n:,0] = model_0.transform_threshold_params(model.params[n:])[1:-1]
    summary.iloc[n:,1] = model_0.transform_threshold_params(model.conf_int()[0][n:])[1:-1]
    summary.iloc[n:,2] = model_0.transform_threshold_params(model.conf_int()[1][n:])[1:-1]
    summary.iloc[n:,3:] = np.nan

    index_change = {}
    for index in summary.index:
        changed = index.replace("/", " / ")
        for var in x_categorical:
            changed = changed.replace("C(%s)" % var, var)
            changed = changed.replace('[T.', ' (')
            changed = changed.replace(']', ')')
        index_change[index] = changed
    summary = summary.rename(index_change)

    result = pd.DataFrame(
        {
            "Pseudo R-Squared": CC(lambda: model.prsquared) ,
            "p-value": CC(lambda: model.llr_pvalue)
        }, index=["Model"]
    )

    add_p(summary)
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def multinomial_logistic_regression(data, x_numeric, x_categorical, y, baseline):
    '''
    Fit an equation that predicts a multinomial categorical variable from other variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one categorical column and several other columns (can be either numeric or categorical).
    x_numeric : :py:class:`list`
        The list of predictor variables that are numeric.
    x_categorical : :py:class:`list`
        The list of predictor variables that are categorical.
    y : :py:class:`str`
        The response variable. Must be categorical.
    baseline : :py:class:`str` or :py:class:`int` or :py:class:`float`
        The baseline group of the categorical variable.
    
    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The coefficients of the fitted equation, along with the confidence intervals, standard errors, z statistics, and p-values.
    result : :py:class:`pandas.DataFrame`
        The pseudo R-squared and p-value of the fitted model.
    
    See also
    --------
    multiple_logistic_regression : Fit an equation that predicts a dichotomous categorical variable from other variables.
    ordered_logistic_regression : Fit an equation that predicts an ordered categorical variable from other variables.
    multiple_linear_regression : Fit an equation that predicts a numeric variable from other variables.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("multinomial_logistic_regression.csv")
    >>> data
         write     ses      prog
    0     35.0     low  vocation
    1     33.0  middle   general
    2     39.0    high  vocation
    3     37.0     low  vocation
    4     31.0  middle  vocation
    ..     ...     ...       ...
    195   65.0    high  academic
    196   63.0  middle  vocation
    197   67.0  middle  academic
    198   65.0  middle  academic
    199   62.0  middle  academic

    We want to fit an equation that predicts *prog* from *write* and *ses*.

    >>> summary, result = bs.multinomial_logistic_regression(data=data, x_numeric=["write"], x_categorical=["ses"], y="prog", baseline="academic")
    >>> summary
                  Coefficient  95% CI: Lower  95% CI: Upper  Std. Error  z Statistic       p-value     
    vocation              NaN            NaN            NaN         NaN          NaN           NaN  NaN
    Intercept        4.235530       1.874390       6.596670    1.204685     3.515881  4.382977e-04  ***
    ses (low)        0.982670      -0.184619       2.149960    0.595567     1.649975  9.894813e-02  NaN
    ses (middle)     1.274063       0.272309       2.275818    0.511109     2.492744  1.267601e-02    *
    write           -0.113603      -0.157153      -0.070052    0.022220    -5.112653  3.176650e-07  ***
                          NaN            NaN            NaN         NaN          NaN           NaN  NaN
    general               NaN            NaN            NaN         NaN          NaN           NaN  NaN
    Intercept        1.689354      -0.715399       4.094108    1.226938     1.376887  1.685473e-01  NaN
    ses (low)        1.162832       0.154980       2.170684    0.514219     2.261354  2.373737e-02    *
    ses (middle)     0.629541      -0.281897       1.540979    0.465028     1.353770  1.758099e-01  NaN
    write           -0.057928      -0.099893      -0.015964    0.021411    -2.705551  6.819115e-03   **
                          NaN            NaN            NaN         NaN          NaN           NaN  NaN

    The coefficients of the fitted equation, along with confidence intervals and p-values are given.

    >>> result
           Pseudo R-Squared       p-value     
    Model          0.118155  1.063001e-08  ***

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
    if data[y].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(y))

    group = data[y].dropna().unique().tolist()
    group.remove(baseline)

    data2 = data[x_numeric+x_categorical].copy()
    data2[y] = 0
    for i, cat in enumerate(group):
        data2.loc[data[y]==cat, y] = i+1

    formula = "%s ~ " % y
    for var in x_numeric:
        formula += "%s + " % var
    for var in x_categorical:
        formula += "C(%s) + " % var
    formula = formula[:-3]

    model = MNLogit.from_formula(formula, data=data2).fit(disp=False)

    summary = pd.DataFrame(columns=["Coefficient", "95% CI: Lower", "95% CI: Upper", "Std. Error", "z Statistic", "p-value"])

    for i, cat in enumerate(group):        
        temp_1 = pd.DataFrame(
            {
                "Coefficient" : np.nan ,
                "95% CI: Lower" : np.nan ,
                "95% CI: Upper" : np.nan ,
                "Std. Error"  : np.nan ,
                "z Statistic" : np.nan ,
                "p-value"     : np.nan ,
            }, index=[cat]
        )
        temp_2 = pd.DataFrame(
            {
                "Coefficient" : CC(lambda: model.params[i]),
                "95% CI: Lower" : CC(lambda: model.conf_int().xs(str(i+1), level=0)["lower"]) ,
                "95% CI: Upper" : CC(lambda: model.conf_int().xs(str(i+1), level=0)["upper"]) ,
                "Std. Error"  : CC(lambda: model.bse[i]),
                "z Statistic" : CC(lambda: model.tvalues[i]),
                "p-value"     : CC(lambda: model.pvalues[i])
            }
        )
        temp_3 = pd.DataFrame(
            {
                "Coefficient" : np.nan ,
                "95% CI: Lower" : np.nan ,
                "95% CI: Upper" : np.nan ,
                "Std. Error"  : np.nan ,
                "z Statistic" : np.nan ,
                "p-value"     : np.nan ,
            }, index=[""]
        )
        summary = pd.concat([summary, temp_1, temp_2, temp_3])
    index_change = {}
    for index in summary.index:
        changed = index.replace("/", " / ")
        for var in x_categorical:
            changed = changed.replace("C(%s)" % var, var)
            changed = changed.replace('[T.', ' (')
            changed = changed.replace(']', ')')
        index_change[index] = changed
    summary = summary.rename(index_change)

    result = pd.DataFrame(
        {
            "Pseudo R-Squared": CC(lambda: model.prsquared),
            "p-value": CC(lambda: model.llr_pvalue)
        }, index=["Model"]
    )

    add_p(summary)
    add_p(result)

    process(summary)
    process(result)

    return summary, result


