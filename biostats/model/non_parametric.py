import numpy as np
import pandas as pd
from scipy import stats as st
import math

from biostats.model.util import _CC, _process, _add_p

class permutation:

    def __init__(self, N, n):
        self.N = N
        self.n = n
        self.s_0 = 0
        self.s_1 = 0
    
    def calc(self):
        self.dfs(0, 1)
        return self.s_1 / self.s_0

    def dfs(self, s, i):
        if i == self.N+1:
            self.s_0 += 1
            if s <= self.n:
                self.s_1 += 1
        else:
            self.dfs(s, i+1)
            self.dfs(s+i, i+1)


def median_test(data, variable, expect):
    '''
    Test whether the mean value of a variable is different from the expected value with nonparametric methods.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column. 
    variable : :py:class:`str`
        The numeric variable that we want to calculate the mean value of.
    expect : :py:class:`float` or :py:class:`int`
        The expected value.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The count, mean value, standard deviation, minimum, first quartile, median, third quartile, and maximum of the variable.
    result : :py:class:`pandas.DataFrame`
        The rank sums, z statistic, and p-values of the normal and exact tests.

    See also
    --------
    wilcoxon_rank_sum_test : Compare the mean values between two groups with nonparametric methods.
    wilcoxon_signed_rank_test : Compare the mean values between two paired groups with nonparametric methods.
    one_sample_t_test : The parametric version of median test.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("median_test.csv")
    >>> data
       Value
    0      3
    1      4
    2      5
    3      4
    4      4
    5      4
    6      4
    7      3
    8      2
    9      5

    We want to test whether the mean value of *Value* is different from 3 with nonparametric methods.

    >>> summary, result = bs.median_test(data=data, variable="Value", expect=3)
    >>> summary
           Count  Mean  Std. Deviation  Minimum  1st Quartile  Median  3rd Quartile  Maximum
    Value     10   3.8        0.918937        2          3.25       4             4        5

    The mean value and some descriptive statistics are given.

    >>> result
            Rank Sum  z Statistic   p-value   
    Normal      32.5      2.05306  0.040067  *
    Exact       32.5          NaN  0.039062  *

    The p-value < 0.05, so the mean value of *Value* is significantly different from the expected value.

    '''

    data = data[[variable]].dropna()
    _process(data, num=[variable])

    if str(data[variable].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(variable))

    summary = pd.DataFrame(
        {
            "Count": _CC(data[variable].count),
            "Mean": _CC(data[variable].mean),
            "Std. Deviation": _CC(data[variable].std,),
            "Minimum": _CC(data[variable].min),
            "1st Quartile": _CC(lambda: data[variable].quantile(0.25)),
            "Median": _CC(data[variable].median),
            "3rd Quartile": _CC(lambda: data[variable].quantile(0.75)),
            "Maximum": _CC(data[variable].max),
        }, index=[variable]
    )

    data_wide = pd.DataFrame(
        {
            "var_1" : data[variable].dropna().tolist() ,
            "var_2" : [expect] * len(data[variable].dropna())
        }
    )
    data_wide["diff"] = data_wide["var_1"] - data_wide["var_2"]
    data_wide = data_wide.drop(data_wide[data_wide["diff"] == 0].index)
    data_wide["abs"] = data_wide["diff"].abs()
    data_wide["rank"] = data_wide["abs"].rank()

    n = _CC(lambda: len(data_wide))
    R = _CC(lambda: data_wide[data_wide["diff"] > 0]["rank"].sum())
    if R == _CC(lambda: n * (n+1) / 4):
        T = 0
    else:
        _t = data_wide["abs"].value_counts().tolist()
        _tsum = 0
        for x in _t:
            _tsum = _CC(lambda: _tsum + x**3 - x)
        T = _CC(lambda: (abs(R - n * (n+1) / 4) - 0.5) / math.sqrt(n * (n+1) * (2*n+1) / 24 - _tsum / 48))
    p = _CC(lambda: 2 * (1 - st.norm.cdf(T)))

    if n < 15:
        exact = permutation(n, int(R))
        _p = _CC(lambda: exact.calc())
        _p = _CC(lambda: 2 * min(_p, 1-_p))
    else:
        _p = np.nan
    
    result = pd.DataFrame(
        {
            "Rank Sum" : [R, R] ,
            "z Statistic" : [T, None] ,
            "p-value" : [p, _p]
        }, index=["Normal", "Exact"]
    )
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result


def sign_test(data, variable, between, group, pair):
    '''
    Test whether the mean values of a variable are different in two paired groups with nonparametric methods.

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
        The counts, mean values, standard deviations, minimums, first quartiles, medians, third quartiles, and maximums of the variable in the two groups.
    result : :py:class:`pandas.DataFrame`
        The sums of sign, z statistic, and p-values of the normal and exact tests.

    See also
    --------
    wilcoxon_signed_rank_test : Similar with sign test but taking the values of difference into account.
    wilcoxon_rank_sum_test : Compare the mean values between two independent groups with nonparametric methods.
    paired_t_test : The parametric version of sign test.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("sign_test.csv")
    >>> data
       Concentration     Month           Clone
    0            8.1    August    Balsam_Spire
    1           10.0    August         Beaupre
    2           16.5    August       Hazendans
    3           13.6    August       Hoogvorst
    4            9.5    August        Raspalje
    5            8.3    August            Unal
    6           18.3    August  Columbia_River
    7           13.3    August   Fritzi_Pauley
    8            7.9    August       Trichobel
    9            8.1    August           Gaver
    10           8.9    August          Gibecq
    11          12.6    August           Primo
    12          13.4    August       Wolterson
    13          11.2  November    Balsam_Spire
    14          16.3  November         Beaupre
    15          15.3  November       Hazendans
    16          15.6  November       Hoogvorst
    17          10.5  November        Raspalje
    18          15.5  November            Unal
    19          12.7  November  Columbia_River
    20          11.1  November   Fritzi_Pauley
    21          19.9  November       Trichobel
    22          20.4  November           Gaver
    23          14.2  November          Gibecq
    24          12.7  November           Primo
    25          36.8  November       Wolterson

    We want to test whether *Concentration* is different between *August* and *November* for every *Clone* with nonparametric methods.

    >>> summary, result = bs.sign_test(data=data, variable="Concentration", between="Month", group=["August", "November"], pair="Clone")
    >>> summary
              Count       Mean  Std. Deviation  Minimum  1st Quartile  Median  3rd Quartile  Maximum
    August       13  11.423077        3.451607      7.9           8.3    10.0          13.4     18.3
    November     13  16.323077        6.886963     10.5          12.7    15.3          16.3     36.8

    The mean values and some descriptive statistics of the two groups are given.

    >>> result
            Sum  z Statistic   p-value      
    Normal    3    -1.664101  0.096092  <NA>
    Exact     3          NaN  0.092285  <NA>

    The p-value > 0.05, so there is no significant difference between *Concentration* of *August* and *November*.

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

    summary = pd.DataFrame(
        {
            "Count": _CC(data.groupby(between, sort=False)[variable].count),
            "Mean": _CC(data.groupby(between, sort=False)[variable].mean),
            "Std. Deviation": _CC(data.groupby(between, sort=False)[variable].std,),
            "Minimum": _CC(data.groupby(between, sort=False)[variable].min),
            "1st Quartile": _CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.25)),
            "Median": _CC(data.groupby(between, sort=False)[variable].median),
            "3rd Quartile": _CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.75)),
            "Maximum": _CC(data.groupby(between, sort=False)[variable].max),
        }
    )
    summary.index.name = None
    summary = summary.reindex(group)

    data_wide = pd.DataFrame(
        {
            "var_1" : data[data[between]==group[0]].sort_values(by=[pair])[variable].tolist() ,
            "var_2" : data[data[between]==group[1]].sort_values(by=[pair])[variable].tolist()
        }
    )
    data_wide["diff"] = data_wide["var_1"] - data_wide["var_2"]
    data_wide = data_wide.drop(data_wide[data_wide["diff"] == 0].index)

    n = _CC(lambda: len(data_wide))
    C = _CC(lambda: data_wide[data_wide["diff"] > 0]["diff"].count())
    if C == n/2 :
        z = 0
        p = 1
    elif C > n/2 :
        z = _CC(lambda: (C- n/2 - 0.5) / math.sqrt(n/4))
        p = _CC(lambda: 2 * (1 - st.norm.cdf(z)))
    else :
        z = _CC(lambda: (C - n/2 + 0.5) / math.sqrt(n/4))
        p = _CC(lambda: 2 * st.norm.cdf(z))

    if n < 20:
        _p = 0
        if C > n/2:
            for x in range(C, n+1):
                _p = _CC(lambda: _p + math.factorial(n) / (math.factorial(x) * math.factorial(n-x) * 2**n))
            _p = _CC(lambda: _p * 2)
        elif C < n/2:
            for x in range(0, C+1):
                _p = _CC(lambda: _p + math.factorial(n) / (math.factorial(x) * math.factorial(n-x) * 2**n))
            _p = _CC(lambda: _p * 2)
        else: 
            _p = 1
    else:
        _p = np.nan
    
    result = pd.DataFrame(
        {
            "Sum" : [C, C] ,
            "z Statistic" : [z, None] ,
            "p-value" : [p, _p]
        }, index=["Normal", "Exact"]
    )
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result


def wilcoxon_signed_rank_test(data, variable, between, group, pair):
    '''
    Test whether the mean values of a variable are different in two paired groups with nonparametric methods.

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
        The counts, mean values, standard deviations, minimums, first quartiles, medians, third quartiles, and maximums of the variable in the two groups.
    result : :py:class:`pandas.DataFrame`
        The rank sums, z statistic, and p-values of the normal and exact tests.

    See also
    --------
    sign_test : Similar with Wilcoxon signed-rank test but not taking the values of difference into account.
    wilcoxon_rank_sum_test : Compare the mean values between two independent groups with nonparametric methods.
    paired_t_test : The parametric version of sign test.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("wilcoxon_signed_rank_test.csv")
    >>> data
       Concentration     Month           Clone
    0            8.1    August    Balsam_Spire
    1           10.0    August         Beaupre
    2           16.5    August       Hazendans
    3           13.6    August       Hoogvorst
    4            9.5    August        Raspalje
    5            8.3    August            Unal
    6           18.3    August  Columbia_River
    7           13.3    August   Fritzi_Pauley
    8            7.9    August       Trichobel
    9            8.1    August           Gaver
    10           8.9    August          Gibecq
    11          12.6    August           Primo
    12          13.4    August       Wolterson
    13          11.2  November    Balsam_Spire
    14          16.3  November         Beaupre
    15          15.3  November       Hazendans
    16          15.6  November       Hoogvorst
    17          10.5  November        Raspalje
    18          15.5  November            Unal
    19          12.7  November  Columbia_River
    20          11.1  November   Fritzi_Pauley
    21          19.9  November       Trichobel
    22          20.4  November           Gaver
    23          14.2  November          Gibecq
    24          12.7  November           Primo
    25          36.8  November       Wolterson

    We want to test whether *Concentration* is different between *August* and *November* for every *Clone* with nonparametric methods.

    >>> summary, result = bs.wilcoxon_signed_rank_test(data=data, variable="Concentration", between="Month", group=["August", "November"], pair="Clone")
    >>> summary
              Count       Mean  Std. Deviation  Minimum  1st Quartile  Median  3rd Quartile  Maximum
    August       13  11.423077        3.451607      7.9           8.3    10.0          13.4     18.3
    November     13  16.323077        6.886963     10.5          12.7    15.3          16.3     36.8

    The mean values and some descriptive statistics of the two groups are given.

    >>> result
            Rank Sum  z Statistic   p-value   
    Normal        16     2.026684  0.042695  *
    Exact         16          NaN  0.039795  *

    The p-value < 0.05, so there is a significant difference between *Concentration* of *August* and *November*.

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

    summary = pd.DataFrame(
        {
            "Count": _CC(data.groupby(between, sort=False)[variable].count),
            "Mean": _CC(data.groupby(between, sort=False)[variable].mean),
            "Std. Deviation": _CC(data.groupby(between, sort=False)[variable].std,),
            "Minimum": _CC(data.groupby(between, sort=False)[variable].min),
            "1st Quartile": _CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.25)),
            "Median": _CC(data.groupby(between, sort=False)[variable].median),
            "3rd Quartile": _CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.75)),
            "Maximum": _CC(data.groupby(between, sort=False)[variable].max),
        }
    )
    summary.index.name = None
    summary = summary.reindex(group)

    data_wide = pd.DataFrame(
        {
            "var_1" : data[data[between]==group[0]].sort_values(by=[pair])[variable].tolist() ,
            "var_2" : data[data[between]==group[1]].sort_values(by=[pair])[variable].tolist()
        }
    )
    data_wide["diff"] = data_wide["var_1"] - data_wide["var_2"]
    data_wide = data_wide.drop(data_wide[data_wide["diff"] == 0].index)
    data_wide["abs"] = data_wide["diff"].abs()
    data_wide["rank"] = data_wide["abs"].rank()

    n = _CC(lambda: len(data_wide))
    R = _CC(lambda: data_wide[data_wide["diff"] > 0]["rank"].sum())
    if R == _CC(lambda: n * (n+1) / 4):
        T = 0
    else:
        _t = data_wide["abs"].value_counts().tolist()
        _tsum = 0
        for x in _t:
            _tsum = _CC(lambda: _tsum + x**3 - x)
        T = _CC(lambda: (abs(R - n * (n+1) / 4) - 0.5) / math.sqrt(n * (n+1) * (2*n+1) / 24 - _tsum / 48))
    p = _CC(lambda: 2 * (1 - st.norm.cdf(T)))

    if n < 15:
        exact = permutation(n, int(R))
        _p = _CC(lambda: exact.calc())
        _p = _CC(lambda: 2 * min(_p, 1-_p))
    else:
        _p = np.nan
    
    result = pd.DataFrame(
        {
            "Rank Sum" : [R, R] ,
            "z Statistic" : [T, None] ,
            "p-value" : [p, _p]
        }, index=["Normal", "Exact"]
    )
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result


def wilcoxon_rank_sum_test(data, variable, between, group):
    '''
    Test whether the mean values of a variable are different in two groups with nonparametric methods.

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

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The counts, mean values, standard deviations, minimums, first quartiles, medians, third quartiles, and maximums of the variable in the two groups.
    result : :py:class:`pandas.DataFrame`
        The rank sums, z statistic, and p-values of the normal and exact tests.

    See also
    --------
    wilcoxon_signed_rank_test : Compare the mean values between two paired groups with nonparametric methods.
    kruskal_wallis_test : Compare the mean values between more than two groups with nonparametric methods.
    two_sample_t_test : The parametric version of Wilcoxon rank-sum test.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("wilcoxon_rank_sum_test.csv")
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

    We want to test whether *value* is different between *2pm* and *5pm* with nonparametric methods.

    >>> summary, result = bs.wilcoxon_rank_sum_test(data=data, variable="Value", between="Time", group=["2pm", "5pm"])
    >>> summary
         Count       Mean  Std. Deviation  Minimum  1st Quartile  Median  3rd Quartile  Maximum
    2pm     18  66.555556        4.889632       59         62.25    66.5         69.75       76
    5pm     16  64.625000        3.667424       59         61.75    64.0         68.00       70

    The mean values and some descriptive statistics of the two groups are given.

    >>> result
            Rank Sum  z Statistic   p-value      
    Normal       357     1.444746  0.148529  <NA>
    Exact        357          NaN       NaN  <NA>

    The p-value > 0.05, so there is no significant difference between the two groups.

    '''

    data = data[list({variable, between})].dropna()
    _process(data, num=[variable], cat=[between])

    if str(data[variable].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))

    data = data[data[between].isin(group)]
    data = data[data[variable].notna()]
    data["rank"] = data[variable].rank()

    summary = pd.DataFrame(
        {
            "Count": _CC(data.groupby(between, sort=False)[variable].count),
            "Mean": _CC(data.groupby(between, sort=False)[variable].mean),
            "Std. Deviation": _CC(data.groupby(between, sort=False)[variable].std,),
            "Minimum": _CC(data.groupby(between, sort=False)[variable].min),
            "1st Quartile": _CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.25)),
            "Median": _CC(data.groupby(between, sort=False)[variable].median),
            "3rd Quartile": _CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.75)),
            "Maximum": _CC(data.groupby(between, sort=False)[variable].max),
        }
    )
    summary.index.name = None
    summary = summary.reindex(group)

    n_1 = _CC(data[data[between]==group[0]]["rank"].count)
    n_2 = _CC(data[data[between]==group[1]]["rank"].count)
    R = _CC(data[data[between]==group[0]]["rank"].sum)
    if R == _CC(lambda: n_1 * (n_1 + n_2 + 1) / 2) :
        T = 0
    else:
        _t = data["rank"].value_counts().tolist()
        _tsum = 0
        for x in _t:
            _tsum = _CC(lambda: _tsum + x**3 - x)
        T = _CC(lambda: (abs(R -n_1*(n_1+n_2+1)/2)-0.5)/math.sqrt((n_1*n_2/12)*(n_1+n_2+1-_tsum/((n_1+n_2)*(n_1+ n_2-1)))))
    p = _CC(lambda: 2 * (1 - st.norm.cdf(T)))

    if n_1 + n_2 < 15:
        exact = permutation(n_1+n_2, int(R))
        _p = _CC(lambda: exact.calc())
        _p = _CC(lambda: 2 * min(_p, 1-_p))
    else:
        _p = np.nan

    result = pd.DataFrame(
        {
            "Rank Sum" : [R, R] ,
            "z Statistic" : [T, None] ,
            "p-value" : [p, _p]
        }, index=["Normal", "Exact"]
    )
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result


def kruskal_wallis_test(data, variable, between):
    '''
    Test whether the mean values of a variable are different between several groups with nonparametric methods.

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
        The counts, mean values, standard deviations, minimums, first quartiles, medians, third quartiles, and maximums of the variable in each group.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, chi-square statistic, and p-value of the test.

    See also
    --------
    one_way_anova : The parametric version of Kruskal-Wallis test.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("kruskal_wallis_test.csv")
    >>> data
        Value    Group
    0       1  Group.1
    1       2  Group.1
    2       3  Group.1
    3       4  Group.1
    4       5  Group.1
    5       6  Group.1
    6       7  Group.1
    7       8  Group.1
    8       9  Group.1
    9      46  Group.1
    10     47  Group.1
    11     48  Group.1
    12     49  Group.1
    13     50  Group.1
    14     51  Group.1
    15     52  Group.1
    16     53  Group.1
    17    342  Group.1
    18     10  Group.2
    19     11  Group.2
    20     12  Group.2
    21     13  Group.2
    22     14  Group.2
    23     15  Group.2
    24     16  Group.2
    25     17  Group.2
    26     18  Group.2
    27     37  Group.2
    28     58  Group.2
    29     59  Group.2
    30     60  Group.2
    31     61  Group.2
    32     62  Group.2
    33     63  Group.2
    34     64  Group.2
    35    193  Group.2
    36     19  Group.3
    37     20  Group.3
    38     21  Group.3
    39     22  Group.3
    40     23  Group.3
    41     24  Group.3
    42     25  Group.3
    43     26  Group.3
    44     27  Group.3
    45     28  Group.3
    46     65  Group.3
    47     66  Group.3
    48     67  Group.3
    49     68  Group.3
    50     69  Group.3
    51     70  Group.3
    52     71  Group.3
    53     72  Group.3

    We want to test whether the mean values of *Value* in each *Group* are different.

    >>> summary, result = bs.kruskal_wallis_test(data=data, variable="Value", between="Group")
    >>> summary
         Group  Count  Mean  Std. Deviation  Minimum  1st Quartile  Median  3rd Quartile  Maximum
    1  Group.1     18  43.5       77.775128        1          5.25    27.5         49.75      342
    2  Group.2     18  43.5       43.694461       10         14.25    27.5         60.75      193
    3  Group.3     18  43.5       23.167548       19         23.25    27.5         67.75       72

    The mean values and some descriptive statistics of each group are given.

    >>> result
           D.F.  Chi Square   p-value   
    Model     2    7.355331  0.025282  *

    The p-value < 0.05, so the mean values of *Value* in each group are significantly different.

    '''

    data = data[list({variable, between})].dropna()
    _process(data, num=[variable], cat=[between])

    if str(data[variable].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))

    summary = pd.DataFrame(
        {
            "{}".format(between) : _CC(data.groupby(between, sort=False)[variable].groups.keys),
            "Count": _CC(data.groupby(between, sort=False)[variable].count),
            "Mean": _CC(data.groupby(between, sort=False)[variable].mean),
            "Std. Deviation": _CC(data.groupby(between, sort=False)[variable].std,),
            "Minimum": _CC(data.groupby(between, sort=False)[variable].min),
            "1st Quartile": _CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.25)),
            "Median": _CC(data.groupby(between, sort=False)[variable].median),
            "3rd Quartile": _CC(lambda: data.groupby(between, sort=False)[variable].quantile(0.75)),
            "Maximum": _CC(data.groupby(between, sort=False)[variable].max),
        }
    )

    summary.index.name = None
    summary = summary.reset_index(drop=True)
    summary.index += 1

    data2 = pd.DataFrame()
    data2[variable] = data[variable].rank(method='average')
    data2[between] = data[between]
    data2 = data2.dropna()

    N = _CC(lambda: len(data2))
    R_i = data2.groupby(between, sort=False)[variable].sum().tolist()
    n_i = data2.groupby(between, sort=False)[variable].count().tolist()
    k = _CC(lambda: len(n_i))

    H = 0
    for i in range(k):
        H = _CC(lambda: H + R_i[i] * R_i[i] / n_i[i])
    H = _CC(lambda: H * 12 / (N * (N + 1)))
    H = _CC(lambda: H - 3 * (N + 1))

    t_i = data2.groupby(variable, sort=False)[variable].count().tolist()
    
    T = 0
    for t in t_i:
        if t > 1:
            T = _CC(lambda: T + t ** 3 - t)
    H = _CC(lambda: H / (1 - T / (N ** 3 - N)))

    p = _CC(lambda: 1 - st.chi2.cdf(H, k-1))

    result = pd.DataFrame(
        {
            "D.F.": _CC(lambda: k-1),
            "Chi Square": _CC(lambda: H),
            "p-value": _CC(lambda: p)
        }, index=["Model"]
    )

    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result


def friedman_test(data, variable, between, subject):
    '''
    Test whether the mean values of a variable are different between several groups on repeated measured data with nonparametric methods.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and one categorical column, as well as a column specifying the subjects.
    variable : :py:class:`str`
        The numeric variable that we want to calculate mean values of.
    between : :py:class:`str`
        The categorical variable that specifies which group the samples belong to. Maximum 20 groups.
    subject : :py:class:`str`
        The variable that specifies the subject ID. Samples measured on the same subject should have the same ID. Maximum 2000 subjects.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The counts, mean values, standard deviations, minimums, first quartiles, medians, third quartiles, and maximums of the variable in each group.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, chi-square statistic, and p-value of the test.

    See also
    --------
    kruskal_wallis_test : Test whether the mean values of a variable are different between groups with nonparametric methods.
    repeated_measures_anova : The parametric version of Friedman Test.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("friedman_test.csv")
    >>> data
        response drug  patient
    0         30    A        1
    1         28    B        1
    2         16    C        1
    3         34    D        1
    4         14    A        2
    5         18    B        2
    6         10    C        2
    7         22    D        2
    8         24    A        3
    9         20    B        3
    10        18    C        3
    11        30    D        3
    12        38    A        4
    13        34    B        4
    14        20    C        4
    15        44    D        4
    16        26    A        5
    17        28    B        5
    18        14    C        5
    19        30    D        5

    We want to test whether the mean values of *response* in each *drug* are different with nonparametric methods, when the samples are repeatedly measured on the four *patient*.

    >>> summary, result = bs.friedman_test(data=data, variable="response", between="drug", subject="patient")
    >>> summary
      drug  Count  Mean  Std. Deviation  Minimum  1st Quartile  Median  3rd Quartile  Maximum
    1    A      5  26.4        8.763561       14            24      26            30       38
    2    B      5  25.6        6.542171       18            20      28            28       34
    3    C      5  15.6        3.847077       10            14      16            18       20
    4    D      5  32.0        8.000000       22            30      30            34       44

    The mean values and some descriptive statistics of each group are given.

    >>> result
           D.F.  Chi Square  p-value    
    Model     3       13.56  0.00357  **

    The p-value < 0.01, so the mean values of *response* in each group are significantly different.

    '''

    data = data[list({variable, between, subject})].dropna()
    _process(data, num=[variable], cat=[between, subject])

    if str(data[variable].dtypes) not in ("float64", "Int64"):
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
        temp = pd.DataFrame(
            {
                "{}".format(between): x,
                "Count": _CC(data[data[between]==x][variable].dropna().count) ,
                "Mean": _CC(data[data[between]==x][variable].dropna().mean) ,
                "Std. Deviation": _CC(data[data[between]==x][variable].dropna().std) ,
                "Minimum": _CC(data[data[between]==x][variable].dropna().min),
                "1st Quartile": _CC(lambda: data[data[between]==x][variable].dropna().quantile(0.25)),
                "Median": _CC(data[data[between]==x][variable].dropna().median),
                "3rd Quartile": _CC(lambda: data[data[between]==x][variable].dropna().quantile(0.75)),
                "Maximum": _CC(data[data[between]==x][variable].dropna().max),
            }, index=[0]
        )
        summary = pd.concat([summary, temp], ignore_index=True)
    summary.index += 1

    data_wide = pd.DataFrame()
    for x in group:
        data_wide[x] = data[data[between]==x].sort_values(by=[subject])[variable].tolist()
    data_wide = data_wide.rank(axis=1)

    k = _CC(lambda: len(data_wide.columns))
    n = _CC(lambda: len(data_wide))
    R_2 = 0
    for col in data_wide.columns:
        r = _CC(lambda: data_wide[col].sum())
        R_2 = _CC(lambda: R_2 + r * r)
    chi2 = _CC(lambda: R_2 * 12 / (n * k * (k + 1)) - 3 * n * (k + 1))
    p = _CC(lambda: 1 - st.chi2.cdf(chi2, k-1))

    result = pd.DataFrame(
        {
            "D.F.": _CC(lambda: k-1),
            "Chi Square": _CC(lambda: chi2),
            "p-value": _CC(lambda: p)
        }, index=["Model"]
    )
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result


def spearman_rank_correlation(data, x, y):
    '''
    Test whether there is a correlation between two numeric variables with nonparametric methods.

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
        The correlation coefficient.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, t statistic, and p-value of the test.
    
    See also
    --------
    correlation : The parametric version of Spearman's rank correlation.
    
    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("spearman_rank_correlation.csv")
    >>> data
        Volume  Pitch
    0     1760    529
    1     2040    566
    2     2440    473
    3     2550    461
    4     2730    465
    5     2740    532
    6     3010    484
    7     3080    527
    8     3370    488
    9     3740    485
    10    4910    478
    11    5090    434
    12    5090    468
    13    5380    449
    14    5850    425
    15    6730    389
    16    6990    421
    17    7960    416

    We want to test whether there is a correlation between *Volume* and *Pitch*.

    >>> summary, result = bs.spearman_rank_correlation(data=data, x="Volume", y="Pitch")
    >>> summary
                 Coefficient
    Correlation    -0.763036

    The correlation coefficient is given.

    >>> result
           D.F.  t Statistic  p-value     
    Model    16    -4.722075  0.00023  ***

    The p-value < 0.001, so there is a significant correlation between *Volume* and *Pitch*.

    '''

    data = data[list({x, y})].dropna()
    _process(data, num=[x, y])
    
    if str(data[x].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(x))
    if str(data[y].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(y))

    data = data[[x,y]].dropna()
    data["rank_x"] = data[x].rank()
    data["rank_y"] = data[y].rank()
    data = data[["rank_x", "rank_y"]]
    r = _CC(lambda: data.corr().iloc[0][1])
    n = _CC(lambda: len(data))

    summary = pd.DataFrame(
        {
            "Coefficient": _CC(lambda: r)
        }, index=["Correlation"]
    )

    t = _CC(lambda: r * math.sqrt((n - 2) / (1 - r * r)))
    p = _CC(lambda: st.t.cdf(t, n-2))
    p = _CC(lambda a: 2*min(a, 1-a), p)

    result = pd.DataFrame(
        {
            "D.F." : _CC(lambda: n-2) ,
            "t Statistic" : _CC(lambda: t) ,
            "p-value" : _CC(lambda: p)
        }, index=["Model"]
    )
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result