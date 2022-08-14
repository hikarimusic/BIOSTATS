import pandas as pd
import numpy as np
from scipy import stats as st
import math

from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

from biostats.model.util import _CC, _process, _add_p

def one_sample_t_test(data, variable, expect, kind="two-side"):
    '''
    Test whether the mean value of a variable is different from the expected value.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column. 
    variable : :py:class:`str`
        The numeric variable that we want to calculate the mean value of.
    expect : :py:class:`float` or :py:class:`int`
        The expected value.
    kind : :py:class:`str`
        * "two-side" : Test whether the mean value is different from the expected value.
        * "greater" : Test whether the mean value is greater than the expected value.
        * "less" : Test whether the mean value is less than the expected value.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The estimation, standard error, and confidence interval of the mean value.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, t statistic, and p-value of the test.

    See also
    --------
    two_sample_t_test : Compare the mean values between two groups.
    paired_t_test : Compare the mean values between two paired groups.
    median_test : The non-parametric version of one-sample t-test.    

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("one_sample_t_test.csv")
    >>> data
       Angle
    0  120.6
    1  116.4
    2  117.2
    3  118.1
    4  114.1
    5  116.9
    6  113.3
    7  121.1
    8  116.9
    9  117.0

    We want to test whether the mean value of *Angle* is different from 120.

    >>> summary, result = bs.one_sample_t_test(data=data, variable="Angle", expect=120, kind="two-side")
    >>> summary
           Estimate  Std. Error  95% CI: Lower  95% CI: Upper
    Angle    117.16    0.769155      115.42005      118.89995

    The mean value of *Angle* and its 95% confidence interval are given.

    >>> result
           D.F.  t Statistic   p-value    
    Model     9    -3.692362  0.004979  **

    The p-value < 0.01, so the mean value of *Angle* is significantly different from the expected value.

    '''

    data = data[[variable]].dropna()
    _process(data, num=[variable])

    if str(data[variable].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(variable))

    n = _CC(lambda a: a.count(), data[variable].dropna())
    mean = _CC(st.tmean, data[variable].dropna())
    sem = _CC(st.tsem, data[variable].dropna())

    if kind == "two-side":
        summary = pd.DataFrame(
            {
                "Estimate" : _CC(lambda: mean) ,
                "Std. Error" : _CC(lambda: sem) ,
                "95% CI: Lower" : _CC(lambda: st.t.ppf(0.025, n-1, mean, sem)) ,
                "95% CI: Upper" : _CC(lambda: st.t.ppf(0.975, n-1, mean, sem)) ,
            }, index=[variable]
        )
        t = _CC(lambda: (mean-expect)/sem)
        p = _CC(lambda: st.t.cdf(t, n-1))
        p = _CC(lambda: 2*min(p, 1-p))
        result = pd.DataFrame(
            {
                "D.F." : _CC(lambda: n-1) ,
                "t Statistic" : _CC(lambda: t) ,
                "p-value" : _CC(lambda: p)
            }, index=["Model"]
        )
    elif kind == "greater":
        summary = pd.DataFrame(
            {
                "Estimate" : _CC(lambda: mean) ,
                "Std. Error" : _CC(lambda: sem) ,
                "95% CI: Lower" : _CC(lambda: st.t.ppf(0.05, n-1, mean, sem)) ,
                "95% CI: Upper" : "Inf" ,
            }, index=[variable]
        )
        t = _CC(lambda: (mean-expect)/sem)
        p = _CC(lambda: st.t.cdf(t, n-1))
        p = _CC(lambda: 1-p)
        result = pd.DataFrame(
            {
                "D.F." : _CC(lambda: n-1) ,
                "t Statistic" : _CC(lambda: t) ,
                "p-value" : _CC(lambda: p)
            }, index=["Model"]
        )
    elif kind == "less":
        summary = pd.DataFrame(
            {
                "Estimate" : _CC(lambda: mean) ,
                "Std. Error" : _CC(lambda: sem) ,
                "95% CI: Lower" : "-Inf" ,
                "95% CI: Upper" : _CC(lambda: st.t.ppf(0.95, n-1, mean, sem)) ,
            }, index=[variable]
        )
        t = _CC(lambda: (mean-expect)/sem)
        p = _CC(lambda: st.t.cdf(t, n-1))
        result = pd.DataFrame(
            {
                "D.F." : _CC(lambda: n-1) ,
                "t Statistic" : _CC(lambda: t) ,
                "p-value" : _CC(lambda: p)
            }, index=["Model"]
        )
    else:
        return

    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result


def two_sample_t_test(data, variable, between, group, kind="equal variances"):
    '''
    Test whether the mean values of a variable are different in two groups.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and one categorical column.
    variable : :py:class:`str`
        The numeric variable that we want to calculate mean values of.
    between : :py:class:`str`
        The categorical variable that specifies which group the samples belong to. Maximum 20 groups.
    group : :py:class:`list`
        List of the two groups to be compared. 
    kind : :py:class:`str`
        * "equal variances" : The normal two-sample t-test which assumes variances of the two groups are equal.
        * "unequal variances" : The variant model in which variances of the two groups can be unequal. Also called Welch's t-test.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The estimations, standard errors, and confidence intervals of the mean values in the two groups, as well as the difference between them.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, t statistic, and p-value of the test.

    See also
    --------
    paired_t_test : Compare the mean values between two paired groups.
    one_way_anova : Compare the mean values between more than two groups.
    wilcoxon_rank_sum_test : The non-parametric version of two-sample t-test.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("two_sample_t_test.csv")
    >>> data
        Value Time
    0      69  2pm
    1      70  2pm
    2      66  2pm
    3      63  2pm
    4      68  2pm
    5      70  2pm
    6      69  2pm
    7      67  2pm
    8      62  2pm
    9      63  2pm
    10     76  2pm
    11     59  2pm
    12     62  2pm
    13     62  2pm
    14     75  2pm
    15     62  2pm
    16     72  2pm
    17     63  2pm
    18     68  5pm
    19     62  5pm
    20     67  5pm
    21     68  5pm
    22     69  5pm
    23     67  5pm
    24     61  5pm
    25     59  5pm
    26     62  5pm
    27     61  5pm
    28     69  5pm
    29     66  5pm
    30     62  5pm
    31     62  5pm
    32     61  5pm
    33     70  5pm

    We want to test whether *value* is different between *2pm* and *5pm*.

    >>> summary, result = bs.two_sample_t_test(data=data, variable="Value", between="Time", group=["2pm", "5pm"], kind="equal variances")
    >>> summary
                 Estimate  Std. Error  95% CI: Lower  95% CI: Upper
    2pm         66.555556    1.152497      64.123999      68.987112
    5pm         64.625000    0.916856      62.670768      66.579232
    Difference   1.930556    1.497923      -1.120613       4.981725

    The mean values of the two groups and the difference between them are given.

    >>> result
           D.F.  t Statistic  p-value      
    Model    32     1.288822   0.2067  <NA>

    The p-value > 0.05, so there is no significant difference between the two groups.

    '''

    data = data[list({variable, between})].dropna()
    _process(data, num=[variable], cat=[between])

    if str(data[variable].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))

    n, mean, std, sem = [None] * 2, [None] * 2, [None] * 2, [None] * 2
    for i, cat, in enumerate(group):
        n[i]    = _CC(data[data[between]==cat][variable].dropna().count)
        mean[i] = _CC(st.tmean, data[data[between]==cat][variable].dropna())
        std[i]  = _CC(st.tstd, data[data[between]==cat][variable].dropna())
        sem[i]  = _CC(st.tsem, data[data[between]==cat][variable].dropna())

    summary = pd.DataFrame(
        {
            "Estimate" : _CC(lambda: mean) ,
            "Std. Error" : _CC(lambda: sem) ,
            "95% CI: Lower" : [_CC(lambda: st.t.ppf(0.025, n[i]-1, mean[i], sem[i])) for i in range(2)] ,
            "95% CI: Upper" : [_CC(lambda: st.t.ppf(0.975, n[i]-1, mean[i], sem[i])) for i in range(2)] ,
        }, index=group
    )

    if kind == "equal variances":
        _mean = _CC(lambda: mean[0]-mean[1])
        _sem = _CC(lambda: math.sqrt(((n[0]-1)*(std[0]**2)+(n[1]-1)*(std[1]**2))*(1/n[0]+1/n[1])/(n[0]+n[1]-2)))
        t = _CC(lambda: _mean/_sem)
        p = _CC(lambda: st.t.cdf(t, n[0]+n[1]-2))
        p = _CC(lambda a: 2*min(a, 1-a), p)

        diff = pd.DataFrame(
            {
                "Estimate" : _CC(lambda: _mean) ,
                "Std. Error" : _CC(lambda: _sem) ,
                "95% CI: Lower" : _CC(lambda: st.t.ppf(0.025, n[0]+n[1]-2, _mean, _sem)) ,
                "95% CI: Upper" : _CC(lambda: st.t.ppf(0.975, n[0]+n[1]-2, _mean, _sem)) ,
            }, index=["Difference"]
        )
        summary = pd.concat([summary, diff])

        result = pd.DataFrame(
            {
                "D.F." : _CC(lambda: n[0]+n[1]-2) ,
                "t Statistic" : _CC(lambda: t) ,
                "p-value" : _CC(lambda: p)
            }, index=["Model"]
        )
    elif kind == "unequal variances":
        _mean = _CC(lambda: mean[0]-mean[1])
        _sem = _CC(lambda: math.sqrt(sem[0]**2+sem[1]**2))
        t = _CC(lambda: _mean/_sem)
        df = _CC(lambda: (sem[0]**2+sem[1]**2)**2/(sem[0]**4/(n[0]-1)+sem[1]**4/(n[1]-1)))
        p = _CC(lambda: st.t.cdf(t, df))
        p = _CC(lambda a: 2*min(a, 1-a), p)

        diff = pd.DataFrame(
            {
                "Estimate" : _CC(lambda: _mean) ,
                "Std. Error" : _CC(lambda: _sem) ,
                "95% CI: Lower" : _CC(lambda: st.t.ppf(0.025, n[0]+n[1]-2, _mean, _sem)) ,
                "95% CI: Upper" : _CC(lambda: st.t.ppf(0.975, n[0]+n[1]-2, _mean, _sem)) ,
            }, index=["Difference"]
        )
        summary = pd.concat([summary, diff])

        result = pd.DataFrame(
            {
                "D.F." : _CC(lambda: df) ,
                "t Statistic" : _CC(lambda: t) ,
                "p-value" : _CC(lambda: p)
            }, index=["Model"]
        )
    else:
        return

    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result


def paired_t_test(data, variable, between, group, pair):
    '''
    Test whether the mean values of a variable are different in two paired groups.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and one categorical column, as well as a column specifying the pairs.
    variable : :py:class:`str`
        The numeric variable that we want to calculate mean values of.
    between : :py:class:`str`
        The categorical variable that specifies which group the samples belong to. Maximum 20 groups.
    group : :py:class:`list`
        List of the two groups to be compared.
    pair : :py:class:`str`
        The variable that specifies the pair ID. Samples in the same pair should have the same ID. Maximum 2000 pairs.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The estimations, standard errors, and confidence intervals of the mean values in the two groups, as well as the difference between them.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, t statistic, and p-value of the test.

    See also
    --------
    two_sample_t_test : Compare the mean values between two independent groups.
    wilcoxon_signed_rank_test : The non-parametric version of paired t-test.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("paired_t_test.csv")
    >>> data
        Length  Feather Bird
    0   -0.255  Typical    A
    1   -0.213  Typical    B
    2   -0.190  Typical    C
    3   -0.185  Typical    D
    4   -0.045  Typical    E
    5   -0.025  Typical    F
    6   -0.015  Typical    G
    7    0.003  Typical    H
    8    0.015  Typical    I
    9    0.020  Typical    J
    10   0.023  Typical    K
    11   0.040  Typical    L
    12   0.040  Typical    M
    13   0.050  Typical    N
    14   0.055  Typical    O
    15   0.058  Typical    P
    16  -0.324      Odd    A
    17  -0.185      Odd    B
    18  -0.299      Odd    C
    19  -0.144      Odd    D
    20  -0.027      Odd    E
    21  -0.039      Odd    F
    22  -0.264      Odd    G
    23  -0.077      Odd    H
    24  -0.017      Odd    I
    25  -0.169      Odd    J
    26  -0.096      Odd    K
    27  -0.330      Odd    L
    28  -0.346      Odd    M
    29  -0.191      Odd    N
    30  -0.128      Odd    O
    31  -0.182      Odd    P

    We want to test whether *Length* is different between *Typical* and *Odd Feather* for every *Bird*.

    >>> summary, result = bs.paired_t_test(data=data, variable="Length", between="Feather", group=["Typical", "Odd"], pair="Bird")
    >>> summary
                Estimate  Std. Error  95% CI: Lower  95% CI: Upper
    Typical    -0.039000    0.026810      -0.096145       0.018145
    Odd        -0.176125    0.027656      -0.235072      -0.117178
    Difference  0.137125    0.033736       0.065218       0.209032

    The mean values of the two groups and the difference between them are given.

    >>> result
           D.F.  t Statistic   p-value    
    Model    15     4.064653  0.001017  **

    The p-value < 0.01, so there is a significant difference between *Length* of the two kinds of *Feather*.

    '''

    data = data[list({variable, between, pair})].dropna()
    _process(data, num=[variable], cat=[between, pair])

    if str(data[variable].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))
    if data[pair].nunique() > 2000:
        raise Warning("The nmuber of classes in column '{}' cannot > 2000.".format(pair))

    data = data[data[between].isin(group)]
    cross = pd.crosstab(index=data[pair], columns=data[between])
    for col in cross:
        cross = cross.drop(cross[cross[col] != 1].index)
    sub = cross.index.values.tolist()
    data = data[data[pair].isin(sub)]

    n, mean, std, sem = [None] * 2, [None] * 2, [None] * 2, [None] * 2
    for i, cat, in enumerate(group):
        n[i]    = _CC(data[data[between]==cat][variable].dropna().count)
        mean[i] = _CC(st.tmean, data[data[between]==cat][variable].dropna())
        std[i]  = _CC(st.tstd, data[data[between]==cat][variable].dropna())
        sem[i]  = _CC(st.tsem, data[data[between]==cat][variable].dropna())

    summary = pd.DataFrame(
        {
            "Estimate" : _CC(lambda: mean) ,
            "Std. Error" : _CC(lambda: sem) ,
            "95% CI: Lower" : [_CC(lambda: st.t.ppf(0.025, n[i]-1, mean[i], sem[i])) for i in range(2)] ,
            "95% CI: Upper" : [_CC(lambda: st.t.ppf(0.975, n[i]-1, mean[i], sem[i])) for i in range(2)] ,
        }, index=group
    )

    data_wide = pd.DataFrame(
        {
            "var_1" : data[data[between]==group[0]].sort_values(by=[pair])[variable].tolist() ,
            "var_2" : data[data[between]==group[1]].sort_values(by=[pair])[variable].tolist()
        }
    )

    diff = data_wide["var_1"] - data_wide["var_2"]
    diff = diff.dropna()

    _n = _CC(lambda a: a.count(), diff.dropna())
    _mean = _CC(st.tmean, diff.dropna())
    _sem = _CC(st.tsem, diff.dropna())

    diff = pd.DataFrame(
        {
            "Estimate" : _CC(lambda: _mean) ,
            "Std. Error" : _CC(lambda: _sem) ,
            "95% CI: Lower" : _CC(lambda: st.t.ppf(0.025, _n-1, _mean, _sem)) ,
            "95% CI: Upper" : _CC(lambda: st.t.ppf(0.975, _n-1, _mean, _sem)) ,
        }, index=["Difference"]
    )
    summary = pd.concat([summary, diff])

    t = _CC(lambda: _mean/_sem)
    p = _CC(lambda: st.t.cdf(t, _n-1))
    p = _CC(lambda a: 2*min(a, 1-a), p)
    result = pd.DataFrame(
        {
            "D.F." : _CC(lambda: _n-1) ,
            "t Statistic" : _CC(lambda: t) ,
            "p-value" : _CC(lambda: p)
        }, index=["Model"]
    )
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result


def pairwise_t_test(data, variable, between):
    '''
    Test whether the mean values of a variable are different between every two groups.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and one categorical column.
    variable : :py:class:`str`
        The numeric variable that we want to calculate mean values of.
    between : :py:class:`str`
        The categorical variable that specifies which group the samples belong to. Maximum 20 groups.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The counts, mean values, standard deviations, and confidence intervals of each group.
    result : :py:class:`pandas.DataFrame`
        The differences, standard errors, t statistics, and p-values of two-sample t-tests on every pair of groups.

    See also
    --------
    one_way_anova : Test whether the mean values are different between groups.
    two_sample_t_test : Test whether the mean values of a variable are different in two groups.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("pairwise_t_test.csv")
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

    We want to perform two-sample t-tests on every pair of *Location*.

    >>> summary, result = bs.pairwise_t_test(data=data, variable="Length", between="Location")
    >>> summary
         Location  Count      Mean  Std. Deviation  95% CI: Lower  95% CI: Upper
    1   Tillamook     10  0.080200        0.011963       0.071642       0.088758
    2     Newport      8  0.074800        0.008597       0.067613       0.081987
    3  Petersburg      7  0.103443        0.016209       0.088452       0.118434
    4     Magadan      8  0.078012        0.012945       0.067190       0.088835
    5   Tvarminne      6  0.095700        0.012962       0.082098       0.109302

    The mean values of *Length* and their 95% confidence intervals in each group are given.

    >>> result
           Group 1     Group 2  Difference  Std. Error  t Statistic   p-value     
    1      Newport   Tillamook   -0.005400    0.005975    -0.903754  1.000000  NaN
    2   Petersburg   Tillamook    0.023243    0.006208     3.744222  0.006696   **
    3      Magadan   Tillamook   -0.002187    0.005975    -0.366104  1.000000  NaN
    4    Tvarminne   Tillamook    0.015500    0.006505     2.382840  0.229125  NaN
    5   Petersburg     Newport    0.028643    0.006519     4.393516  0.001034   **
    6      Magadan     Newport    0.003213    0.006298     0.510059  1.000000  NaN
    7    Tvarminne     Newport    0.020900    0.006803     3.072207  0.041651    *
    8      Magadan  Petersburg   -0.025430    0.006519    -3.900752  0.004300   **
    9    Tvarminne  Petersburg   -0.007743    0.007008    -1.104846  1.000000  NaN
    10   Tvarminne     Magadan    0.017688    0.006803     2.599983  0.136962  NaN

    The p-values of *Petersburg/Tillamook*, *Petersburg/Newport*, *Petersburg/Magadan*, and *Newport/Tvarminne* < 0.05, so the differences of mean values in these pairs of groups are significant.

    '''

    data = data[list({variable, between})].dropna()
    _process(data, num=[variable], cat=[between])

    if str(data[variable].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))

    group = data[between].dropna().unique()

    summary = pd.DataFrame()

    for x in group:
        n = _CC(data[data[between]==x][variable].dropna().count)
        mean = _CC(data[data[between]==x][variable].dropna().mean)
        std = _CC(data[data[between]==x][variable].dropna().std)
        sem = _CC(data[data[between]==x][variable].dropna().sem)
        temp = pd.DataFrame(
            {
                "{}".format(between): x,
                "Count": _CC(lambda: n),
                "Mean": _CC(lambda: mean),
                "Std. Deviation": _CC(lambda: std),
                "95% CI: Lower" : _CC(lambda: st.t.ppf(0.025, n-1, mean, sem)) ,
                "95% CI: Upper" : _CC(lambda: st.t.ppf(0.975, n-1, mean, sem)) ,
            }, index=[0]
        )
        summary = pd.concat([summary, temp], ignore_index=True)
    summary.index += 1
    result = pd.DataFrame()
    group = data[between].dropna().unique()
    df = _CC(lambda: len(data[[variable, between]].dropna()) - len(group))
    corr = _CC(lambda: len(group) * (len(group) - 1) / 2)

    formula = "Q('%s') ~ " % variable
    formula += "C(Q('%s'))" % between
    model = ols(formula, data=data).fit()
    anova = anova_lm(model)
    s = _CC(lambda: math.sqrt(anova["mean_sq"][1]))

    for i in range(0, len(group)):
        for j in range(i+1, len(group)):
            n, mean, std = [None] * 2, [None] * 2, [None] * 2
            for k, cat, in enumerate([group[j], group[i]]):
                n[k]    = _CC(data[data[between]==cat][variable].count)
                mean[k] = _CC(st.tmean, data[data[between]==cat][variable].dropna())
                std[k]  = _CC(st.tstd, data[data[between]==cat][variable].dropna())
            diff = _CC(lambda: mean[0]-mean[1])
            sem = _CC(lambda: s*math.sqrt(1/n[0]+1/n[1]))
            t = _CC(lambda: diff/sem)
            p = _CC(lambda: st.t.cdf(t, df))
            p = _CC(lambda a: 2*min(a, 1-a), p)
            p = _CC(lambda: p*corr)
            if p > 1:
                p = 1
            temp = pd.DataFrame(
                {
                    "Group 1" : _CC(lambda: group[j]),
                    "Group 2" : _CC(lambda: group[i]),
                    "Difference" : _CC(lambda: diff),
                    "Std. Error" : _CC(lambda: sem),
                    "t Statistic" : _CC(lambda: t),
                    "p-value" : _CC(lambda: p)
                }, index=[0]
            )
            result = pd.concat([result, temp], ignore_index=True)

    _add_p(result)
    result.index += 1

    _process(summary)
    _process(result)

    return summary, result        



