import numpy as np
import pandas as pd
from scipy import stats as st

from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.multivariate.manova import MANOVA

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

def one_way_anova(data, variable, between):
    '''
    Test whether the mean values of a variable are defferent in several groups.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must Contain at least one numeric column and one categorical column.
    variable : :py:class:`str`
        The name of the *variable* column. The means of values in the *variable* column are our targets.
    between : :py:class:`str`
        The name of the *between* column. Values in the *between* column indicate which group a sample belongs to.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The counts, mean values, standard deviations, and confidence intervals of each group.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, chi square statistic, and p-value of the test.

    See also
    --------
    two_way_anova : Test whether the mean values are different in groups, classified in two ways.
    one_way_ancova : Test whether the mean values are different in groups, when another variable is controlled.
    kruskal_wallis_test : The non-parametric alternative to one-way ANOVA.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("one_way_anova.csv")
    >>> data
        Length    Location
    0   0.0571   Tillamook
    1   0.0813   Tillamook
    2   0.0831   Tillamook
    3   0.0976   Tillamook
    4   0.0817   Tillamook
    5   0.0859   Tillamook
    6   0.0735   Tillamook
    7   0.0659   Tillamook
    8   0.0923   Tillamook
    9   0.0836   Tillamook
    10  0.0873     Newport
    11  0.0662     Newport
    12  0.0672     Newport
    13  0.0819     Newport
    14  0.0749     Newport
    15  0.0649     Newport
    16  0.0835     Newport
    17  0.0725     Newport
    18  0.0974  Petersburg
    19  0.1352  Petersburg
    20  0.0817  Petersburg
    21  0.1016  Petersburg
    22  0.0968  Petersburg
    23  0.1064  Petersburg
    24  0.1050  Petersburg
    25  0.1033     Magadan
    26  0.0915     Magadan
    27  0.0781     Magadan
    28  0.0685     Magadan
    29  0.0677     Magadan
    30  0.0697     Magadan
    31  0.0764     Magadan
    32  0.0689     Magadan
    33  0.0703   Tvarminne
    34  0.1026   Tvarminne
    35  0.0956   Tvarminne
    36  0.0973   Tvarminne
    37  0.1039   Tvarminne
    38  0.1045   Tvarminne

    We want to test whether the mean values of *Length* in each *Location* are different.

    >>> summary, result = bs.one_way_anova(data=data, variable="Length", between="Location")
    >>> summary
         Location  Count      Mean  Std. Deviation  95% CI: Lower  95% CI: Upper
    1   Tillamook   10.0  0.080200        0.011963       0.071642       0.088758
    2     Newport    8.0  0.074800        0.008597       0.067613       0.081987
    3  Petersburg    7.0  0.103443        0.016209       0.088452       0.118434
    4     Magadan    8.0  0.078012        0.012945       0.067190       0.088835
    5   Tvarminne    6.0  0.095700        0.012962       0.082098       0.109302

    The mean values of *Length* and their 95% confidence intervals in each group are given.

    >>> result
              D.F.  Sum Square  Mean Square  F Statistic   p-value     
    Location   4.0    0.004520     0.001130     7.121019  0.000281  ***
    Residual  34.0    0.005395     0.000159          NaN       NaN  NaN

    The p-value < 0.001, so the mean values of *Length* in each group are significantly different.

    '''

    process(data)
    data = data[list({variable, between})].dropna()

    if str(data[variable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))

    group = data[between].dropna().unique()

    summary = pd.DataFrame()

    for x in group:
        n = CC(lambda: data[data[between]==x][variable].dropna().count())
        mean = CC(lambda: data[data[between]==x][variable].dropna().mean())
        std = CC(lambda: data[data[between]==x][variable].dropna().std())
        sem = CC(lambda: data[data[between]==x][variable].dropna().sem())
        temp = pd.DataFrame(
            {
                "{}".format(between): CC(lambda: x),
                "Count": CC(lambda: n),
                "Mean": CC(lambda: mean),
                "Std. Deviation": CC(lambda: std),
                "95% CI: Lower" : CC(lambda: st.t.ppf(0.025, n-1, mean, sem)) ,
                "95% CI: Upper" : CC(lambda: st.t.ppf(0.975, n-1, mean, sem)) ,
            }, index=[0]
        )
        summary = pd.concat([summary, temp], ignore_index=True)
    summary.index += 1

    formula = "Q('%s') ~ " % variable
    formula += "C(Q('%s'))" % between
    model = ols(formula, data=data).fit()
    result = anova_lm(model)
    result = result.rename(columns={
        'df': 'D.F.',
        'sum_sq' : 'Sum Square',
        'mean_sq' : 'Mean Square',
        'F' : 'F Statistic',
        'PR(>F)' : 'p-value'
    })
    result = result.rename(index={
        "C(Q('%s'))" % between : between
    })
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def two_way_anova(data, variable, between_1, between_2):

    process(data)
    data = data[list({variable, between_1, between_2})].dropna()

    if str(data[variable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between_1].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between_1))
    if data[between_2].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between_2))

    group_1 = data[between_1].dropna().unique()
    group_2 = data[between_2].dropna().unique()

    summary = pd.DataFrame()

    for x in group_1:
        for y in group_2:
            n = CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][variable].dropna().count())
            mean = CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][variable].dropna().mean())
            std = CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][variable].dropna().std())
            sem = CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][variable].dropna().sem())
            temp = pd.DataFrame(
                {
                    "{}".format(between_1): CC(lambda: x),
                    "{}".format(between_2): CC(lambda: y),
                    "Count": CC(lambda: n),
                    "Mean": CC(lambda: mean),
                    "Std. Deviation": CC(lambda: std),
                    "95% CI: Lower" : CC(lambda: st.t.ppf(0.025, n-1, mean, sem)) ,
                    "95% CI: Upper" : CC(lambda: st.t.ppf(0.975, n-1, mean, sem)) ,
                }, index=[0]
            )
            summary = pd.concat([summary, temp], ignore_index=True)
    summary.index += 1

    formula = "Q('%s') ~ " % variable
    formula += "C(Q('%s'), Sum) * " % between_1
    formula += "C(Q('%s'), Sum)" % between_2
    model = ols(formula, data=data).fit()
    result = anova_lm(model)
    result = result.rename(columns={
        'df': 'D.F.',
        'sum_sq' : 'Sum Square',
        'mean_sq' : 'Mean Square',
        'F' : 'F Statistic',
        'PR(>F)' : 'p-value'
    })
    index_change = {}
    for index in result.index:
        changed = index
        changed = changed.replace("C(Q('%s'), Sum)" % between_1, between_1)
        changed = changed.replace("C(Q('%s'), Sum)" % between_2, between_2)
        changed = changed.replace(":", " : ")
        index_change[index] = changed
    result = result.rename(index_change)
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def one_way_ancova(data, variable, between, covariable):

    process(data)
    data = data[list({variable, between, covariable})].dropna()

    if str(data[variable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))
    if str(data[covariable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(covariable))

    group = data[between].dropna().unique()

    summary = pd.DataFrame()

    for x in group:
        n = CC(lambda: data[data[between]==x][[variable, covariable]].dropna()[variable].count())
        mean_1 = CC(lambda: data[data[between]==x][[variable, covariable]].dropna()[variable].mean())
        std_1 = CC(lambda: data[data[between]==x][[variable, covariable]].dropna()[variable].std())
        mean_2 = CC(lambda: data[data[between]==x][[variable, covariable]].dropna()[covariable].mean())
        std_2 = CC(lambda: data[data[between]==x][[variable, covariable]].dropna()[covariable].std())
        temp = pd.DataFrame(
            {
                "{}".format(between): x,
                "Count": n,
                "Mean ({})".format(variable): CC(lambda: mean_1),
                "Std. ({})".format(variable): CC(lambda: std_1),
                "Mean ({})".format(covariable): CC(lambda: mean_2),
                "Std. ({})".format(covariable): CC(lambda: std_2),
            }, index=[0]
        )
        summary = pd.concat([summary, temp], ignore_index=True)
    summary.index += 1

    formula = "Q('%s') ~ " % variable
    formula += "C(Q('%s'), Sum) + " % between
    formula += "Q('%s')" % covariable
    model = ols(formula, data=data).fit()

    result = anova_lm(model, typ=2)
    result = result.rename(columns={
        'df': 'D.F.',
        'sum_sq' : 'Sum Square',
        'F' : 'F Statistic',
        'PR(>F)' : 'p-value'
    })
    index_change = {}
    for index in result.index:
        changed = index
        changed = changed.replace("C(Q('%s'), Sum)" % between, between)
        changed = changed.replace("Q('%s')" % covariable, covariable)
        index_change[index] = changed
    result = result.rename(index_change)
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def two_way_ancova(data, variable, between_1, between_2, covariable):

    process(data)
    data = data[list({variable, between_1, between_2, covariable})].dropna()

    if str(data[variable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between_1].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between_1))
    if data[between_2].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between_2))
    if str(data[covariable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(covariable))

    group_1 = data[between_1].dropna().unique()
    group_2 = data[between_2].dropna().unique()

    summary = pd.DataFrame()


    summary = pd.DataFrame()

    for x in group_1:
        for y in group_2:
            n = CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][[variable, covariable]].dropna()[variable].count())
            mean_1 = CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][[variable, covariable]].dropna()[variable].mean())
            std_1 = CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][[variable, covariable]].dropna()[variable].std())
            mean_2 = CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][[variable, covariable]].dropna()[covariable].mean())
            std_2 = CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][[variable, covariable]].dropna()[covariable].std())
            temp = pd.DataFrame(
                {
                    "{}".format(between_1): CC(lambda: x),
                    "{}".format(between_2): CC(lambda: y),
                    "Count": CC(lambda: n),
                    "Mean ({})".format(variable): CC(lambda: mean_1),
                    "Std. ({})".format(variable): CC(lambda: std_1),
                    "Mean ({})".format(covariable): CC(lambda: mean_2),
                    "Std. ({})".format(covariable): CC(lambda: std_2),
                }, index=[0]
            )
            summary = pd.concat([summary, temp], ignore_index=True)
    summary.index += 1

    formula = "Q('%s') ~ " % variable
    formula += "C(Q('%s'), Sum) * " % between_1
    formula += "C(Q('%s'), Sum) + " % between_2
    formula += "Q('%s')" % covariable
    model = ols(formula, data=data).fit()

    result = anova_lm(model, typ=2)
    result = result.rename(columns={
        'df': 'D.F.',
        'sum_sq' : 'Sum Square',
        'F' : 'F Statistic',
        'PR(>F)' : 'p-value'
    })
    index_change = {}
    for index in result.index:
        changed = index
        changed = changed.replace("C(Q('%s'), Sum)" % between_1, between_1)
        changed = changed.replace("C(Q('%s'), Sum)" % between_2, between_2)
        changed = changed.replace("Q('%s')" % covariable, covariable)
        changed = changed.replace(":", " : ")
        index_change[index] = changed
    result = result.rename(index_change)
    add_p(result)

    process(summary)
    process(result)

    return summary, result

def multivariate_anova(data, variable, between):

    process(data)
    data = data[list(set(variable + [between]))].dropna()

    for var in variable:
        if str(data[var].dtypes) != "float64":
            raise Warning("The column '{}' must be numeric".format(var))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))

    group = data[between].dropna().unique().tolist()

    summary = pd.DataFrame({between:group})
    for var in variable:
        mean = []
        std = []
        for x in group:
            mean.append(CC(lambda: data[data[between]==x][var].dropna().mean()))
            std.append(CC(lambda: data[data[between]==x][var].dropna().std()))
        summary["Mean ({})".format(var)] = mean
        summary["Std. ({})".format(var)] = std  
    summary.index += 1 

    formula = ""
    for var in variable:
        formula += "{} + ".format(var)
    formula = formula[:-3]
    formula += " ~ {}".format(between)
    fit = MANOVA.from_formula(formula, data=data)
    table = pd.DataFrame((fit.mv_test().results[between]['stat']))
    result = pd.DataFrame(
        {
            "D.F." : CC(lambda: len(group)-1) ,
            "Pillai's Trace" : CC(lambda: table.iloc[1][0]) ,
            "F Statistic" : CC(lambda: table.iloc[1][3]) ,
            "p-value" : CC(lambda: table.iloc[1][4])
        }, index=[between]
    )
    add_p(result)

    process(summary)
    process(result)

    return summary, result

def repeated_measures_anova(data, variable, between, subject):

    process(data)
    data = data[list({variable, between, subject})].dropna()

    if str(data[variable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))
    if data[subject].nunique() > 2000:
        raise Warning("The nmuber of classes in column '{}' cannot > 2000.".format(subject))

    cross = pd.crosstab(index=data[subject], columns=data[between])
    for col in cross:
        cross = cross.drop(cross[cross[col] != 1].index)
    sub = cross.index.values.tolist()
    data = data[data[subject].isin(sub)]
    
    group = data[between].dropna().unique()

    summary = pd.DataFrame()

    for x in group:
        n = CC(lambda: data[data[between]==x][variable].dropna().count())
        mean = CC(lambda: data[data[between]==x][variable].dropna().mean())
        std = CC(lambda: data[data[between]==x][variable].dropna().std())
        sem = CC(lambda: data[data[between]==x][variable].dropna().sem())
        temp = pd.DataFrame(
            {
                "{}".format(between): CC(lambda: x),
                "Count": CC(lambda: n),
                "Mean": CC(lambda: mean),
                "Std. Deviation": CC(lambda: std),
                "95% CI: Lower" : CC(lambda: st.t.ppf(0.025, n-1, mean, sem)) ,
                "95% CI: Upper" : CC(lambda: st.t.ppf(0.975, n-1, mean, sem)) ,
            }, index=[0]
        )
        summary = pd.concat([summary, temp], ignore_index=True)
    summary.index += 1

    formula = "Q('%s') ~ " % variable
    formula += "C(Q('%s'))" % between
    model = ols(formula, data=data).fit()
    anova_1 = anova_lm(model)
    formula = "Q('%s') ~ " % variable
    formula += "C(Q('%s'))" % subject
    model = ols(formula, data=data).fit()
    anova_2 = anova_lm(model)

    df_1 = CC(lambda: anova_1.iloc[0][0])
    df_2 = CC(lambda: df_1 * anova_2.iloc[0][0])
    SS_1 = CC(lambda: anova_1.iloc[0][1])
    SS_2 = CC(lambda: anova_2.iloc[1][1] - SS_1)
    MS_1 = CC(lambda: SS_1 / df_1)
    MS_2 = CC(lambda: SS_2 / df_2)
    F = CC(lambda: MS_1 / MS_2)
    p = CC(lambda: 1 - st.f.cdf(F, df_1, df_2))

    result = pd.DataFrame(
        {
            "D.F." : [df_1, df_2] ,
            "Sum Square" : [SS_1, SS_2] ,
            "Mean Square" : [MS_1, MS_2] ,
            "F Statistic" : [F, None] ,
            "p-value" : [p, None]
        }, index = [between, "Residual"]
    )
    add_p(result)

    process(summary)
    process(result)

    return summary, result

