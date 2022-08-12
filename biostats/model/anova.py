import pandas as pd
from scipy import stats as st

from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.multivariate.manova import MANOVA

from biostats.model.util import _CC, _process, _add_p

def one_way_anova(data, variable, between):
    '''
    Test whether the mean values of a variable are different between several groups.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and one categorical column.
    variable : :py:class:`str`
        The numeric variable that we want to calculate mean values of.
    between : :py:class:`str`
        The categorical variable that specifies which group the samples belong to.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The counts, mean values, standard deviations, and confidence intervals of each group.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, sum of squares, mean of squares, F statistic, and p-value of the test.

    See also
    --------
    one_way_ancova : Test whether the mean values are different between groups, when another variable is controlled.
    two_way_anova : Test whether the mean values are different between groups, when classified in two ways.
    kruskal_wallis_test : The non-parametric version of one-way ANOVA.

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
    1   Tillamook     10  0.080200        0.011963       0.071642       0.088758
    2     Newport      8  0.074800        0.008597       0.067613       0.081987
    3  Petersburg      7  0.103443        0.016209       0.088452       0.118434
    4     Magadan      8  0.078012        0.012945       0.067190       0.088835
    5   Tvarminne      6  0.095700        0.012962       0.082098       0.109302

    The mean values of *Length* and their 95% confidence intervals in each group are given.

    >>> result
              D.F.  Sum Square  Mean Square  F Statistic   p-value     
    Location     4    0.004520     0.001130     7.121019  0.000281  ***
    Residual    34    0.005395     0.000159          NaN       NaN  NaN

    The p-value < 0.001, so the mean values of *Length* in each group are significantly different.

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
        n = _CC(lambda: data[data[between]==x][variable].dropna().count())
        mean = _CC(lambda: data[data[between]==x][variable].dropna().mean())
        std = _CC(lambda: data[data[between]==x][variable].dropna().std())
        sem = _CC(lambda: data[data[between]==x][variable].dropna().sem())
        temp = pd.DataFrame(
            {
                "{}".format(between): _CC(lambda: x),
                "Count": _CC(lambda: n),
                "Mean": _CC(lambda: mean),
                "Std. Deviation": _CC(lambda: std),
                "95% CI: Lower" : _CC(lambda: st.t.ppf(0.025, n-1, mean, sem)) ,
                "95% CI: Upper" : _CC(lambda: st.t.ppf(0.975, n-1, mean, sem)) ,
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
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result


def two_way_anova(data, variable, between_1, between_2):
    '''
    Test whether the mean values of a variable are different between several groups, when the groups are classified in two ways.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and two categorical columns.
    variable : :py:class:`str`
        The numeric variable that we want to calculate mean values of.
    between_1 : :py:class:`str`
        The first categorical variable that specifies the groups of the samples.
    between_2 : :py:class:`str`
        The second categorical variable that specifies the groups of the samples.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The counts, mean values, standard deviations, and confidence intervals of each combination of groups.
    result : :py:class:`pandas.DataFrame`
        The degrees of freedom, sums of squares, means of squares, F statistics, and p-values of the test.

    See also
    --------
    two_way_ancova : Two-way ANOVA with another variable being controlled. 
    one_way_anova : Test whether the mean values are different between groups.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("two_way_anova.csv")
    >>> data
        Activity     Sex Genotype
    0      1.884    male       ff
    1      2.283    male       ff
    2      2.396    male       fs
    3      2.838  female       ff
    4      2.956    male       fs
    5      4.216  female       ff
    6      3.620  female       ss
    7      2.889  female       ff
    8      3.550  female       fs
    9      3.105    male       fs
    10     4.556  female       fs
    11     3.087  female       fs
    12     4.939    male       ff
    13     3.486    male       ff
    14     3.079  female       ss
    15     2.649    male       fs
    16     1.943  female       fs
    17     4.198  female       ff
    18     2.473  female       ff
    19     2.033  female       ff
    20     2.200  female       fs
    21     2.157  female       fs
    22     2.801    male       ss
    23     3.421    male       ss
    24     1.811  female       ff
    25     4.281  female       fs
    26     4.772  female       fs
    27     3.586  female       ss
    28     3.944  female       ff
    29     2.669  female       ss
    30     3.050  female       ss
    31     4.275    male       ss
    32     2.963  female       ss
    33     3.236  female       ss
    34     3.673  female       ss
    35     3.110    male       ss

    We want to test that whether the mean values of *Activity* are different between *male* and *female*, and between *ff*, *fs* and *ss*. We also want to test that whether there is an interaction between *Sex* and *Genotype*.

    >>> summary, result = bs.two_way_anova(data=data, variable="Activity", between_1="Sex", between_2="Genotype")
    >>> summary
          Sex Genotype  Count     Mean  Std. Deviation  95% CI: Lower  95% CI: Upper
    1    male       ff      4  3.14800        1.374512       0.960845       5.335155
    2    male       fs      4  2.77650        0.316843       2.272332       3.280668
    3    male       ss      4  3.40175        0.634811       2.391624       4.411876
    4  female       ff      8  3.05025        0.959903       2.247751       3.852749
    5  female       fs      8  3.31825        1.144539       2.361392       4.275108
    6  female       ss      8  3.23450        0.361775       2.932048       3.536952

    The mean values and 95% confidence intervals of each combination of *Sex* and *Genotype* are given.

    >>> result
                    D.F.  Sum Square  Mean Square  F Statistic   p-value      
    Sex                1    0.068080     0.068080     0.086128  0.771180  <NA>
    Genotype           2    0.277240     0.138620     0.175366  0.840004  <NA>
    Sex : Genotype     2    0.814641     0.407321     0.515295  0.602515  <NA>
    Residual          30   23.713823     0.790461          NaN       NaN  <NA>

    The p-value of *Sex* > 0.05, so *Activity* are not different between the two *Sex*. The p-value of *Genotype* > 0.05, so *Activity* are not different between the three *Genotype*. The p-value of interaction > 0.05, so there is no interaction between *Sex* and *Genotype*. 

    '''

    data = data[list({variable, between_1, between_2})].dropna()
    _process(data, num=[variable], cat=[between_1, between_2])

    if str(data[variable].dtypes) not in ("float64", "Int64"):
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
            n = _CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][variable].dropna().count())
            mean = _CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][variable].dropna().mean())
            std = _CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][variable].dropna().std())
            sem = _CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][variable].dropna().sem())
            temp = pd.DataFrame(
                {
                    "{}".format(between_1): _CC(lambda: x),
                    "{}".format(between_2): _CC(lambda: y),
                    "Count": _CC(lambda: n),
                    "Mean": _CC(lambda: mean),
                    "Std. Deviation": _CC(lambda: std),
                    "95% CI: Lower" : _CC(lambda: st.t.ppf(0.025, n-1, mean, sem)) ,
                    "95% CI: Upper" : _CC(lambda: st.t.ppf(0.975, n-1, mean, sem)) ,
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
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result


def one_way_ancova(data, variable, between, covariable):
    '''
    Test whether the mean values of a variable are different between several groups, when another variable is controlled.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two numeric columns and one categorical column.
    variable : :py:class:`str`
        The numeric variable that we want to calculate mean values of.
    between : :py:class:`str`
        The categorical variable that specifies which group the samples belong to.
    covariable : :py:class:`str`
        Another numeric variable that we want to control.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The counts, mean values and standard deviations of the variable, and that of the covariable in each group.
    result : :py:class:`pandas.DataFrame`
        The sums of squares, degrees of freedom, F statistics, and p-values of the test.

    See also
    --------
    one_way_anova : Test whether the mean values are different between groups.
    two_way_ancova : Test whether the mean values are different between groups classified in two ways, when another variable is controlled.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("one_way_ancova.csv")
    >>> data
        Pulse Species  Temp
    0    67.9      ex  20.8
    1    65.1      ex  20.8
    2    77.3      ex  24.0
    3    78.7      ex  24.0
    4    79.4      ex  24.0
    5    80.4      ex  24.0
    6    85.8      ex  26.2
    7    86.6      ex  26.2
    8    87.5      ex  26.2
    9    89.1      ex  26.2
    10   98.6      ex  28.4
    11  100.8      ex  29.0
    12   99.3      ex  30.4
    13  101.7      ex  30.4
    14   44.3     niv  17.2
    15   47.2     niv  18.3
    16   47.6     niv  18.3
    17   49.6     niv  18.3
    18   50.3     niv  18.9
    19   51.8     niv  18.9
    20   60.0     niv  20.4
    21   58.5     niv  21.0
    22   58.9     niv  21.0
    23   60.7     niv  22.1
    24   69.8     niv  23.5
    25   70.9     niv  24.2
    26   76.2     niv  25.9
    27   76.1     niv  26.5
    28   77.0     niv  26.5
    29   77.7     niv  26.5
    30   84.7     niv  28.6
    31   74.3    fake  17.2
    32   77.2    fake  18.3
    33   77.6    fake  18.3
    34   79.6    fake  18.3
    35   80.3    fake  18.9
    36   81.8    fake  18.9
    37   90.0    fake  20.4
    38   88.5    fake  21.0
    39   88.9    fake  21.0
    40   90.7    fake  22.1
    41   99.8    fake  23.5
    42  100.9    fake  24.2
    43  106.2    fake  25.9
    44  106.1    fake  26.5
    45  107.0    fake  26.5
    46  107.7    fake  26.5
    47  114.7    fake  28.6

    We want to test whether the mean values of *Pulse* ar different between the three *Species*, with *Temp* being controlled.

    >>> summary, result = bs.one_way_ancova(data=data, variable="Pulse", between="Species", covariable="Temp")
    >>> summary
      Species  Count  Mean (Pulse)  Std. (Pulse)  Mean (Temp)  Std. (Temp)
    1      ex     14     85.585714      11.69930    25.757143     3.074639
    2     niv     17     62.429412      12.95684    22.123529     3.659325
    3    fake     17     92.429412      12.95684    22.123529     3.659325

    The mean values of *Pulse* and *Temp* in each group are given.

    >>> result
               Sum Square  D.F.  F Statistic       p-value     
    Species   7835.737962     2  1372.995165  2.252680e-40  ***
    Temp      7025.952857     1  2462.205692  2.877499e-40  ***
    Residual   125.554874    44          NaN           NaN  NaN

    The p-value of *Species* < 0.05, so the mean values of *Pulse* are different between the three *Species*, even after *Temp* being controlled.

    '''

    data = data[list({variable, between, covariable})].dropna()
    _process(data, num=[variable, covariable], cat=[between])

    if str(data[variable].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))
    if str(data[covariable].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(covariable))

    group = data[between].dropna().unique()

    summary = pd.DataFrame()

    for x in group:
        n = _CC(lambda: data[data[between]==x][[variable, covariable]].dropna()[variable].count())
        mean_1 = _CC(lambda: data[data[between]==x][[variable, covariable]].dropna()[variable].mean())
        std_1 = _CC(lambda: data[data[between]==x][[variable, covariable]].dropna()[variable].std())
        mean_2 = _CC(lambda: data[data[between]==x][[variable, covariable]].dropna()[covariable].mean())
        std_2 = _CC(lambda: data[data[between]==x][[variable, covariable]].dropna()[covariable].std())
        temp = pd.DataFrame(
            {
                "{}".format(between): x,
                "Count": n,
                "Mean ({})".format(variable): _CC(lambda: mean_1),
                "Std. ({})".format(variable): _CC(lambda: std_1),
                "Mean ({})".format(covariable): _CC(lambda: mean_2),
                "Std. ({})".format(covariable): _CC(lambda: std_2),
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
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result


def two_way_ancova(data, variable, between_1, between_2, covariable):
    '''
    Test whether the mean values of a variable are different between several groups classified in two ways, when another variable is controlled.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two numeric columns and two categorical columns.
    variable : :py:class:`str`
        The numeric variable that we want to calculate mean values of.
    between_1 : :py:class:`str`
        The first categorical variable that specifies the groups of the samples.
    between_2 : :py:class:`str`
        The second categorical variable that specifies the groups of the samples.
    covariable : :py:class:`str`
        Another numeric variable that we want to control.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The counts, mean values and standard deviations of the variable, and that of the covariable in each combination of groups.
    result : :py:class:`pandas.DataFrame`
        The sums of squares, degrees of freedom, F statistics, and p-values of the test.

    See also
    --------
    two_way_anova : Test whether the mean values are different between several groups classified in two ways.
    one_way_ancova : Test whether the mean values are different between groups, when another variable is controlled.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("two_way_ancova.csv")
    >>> data
        Activity     Sex Genotype  Age
    0      1.884    male       ff   69
    1      2.283    male       ff   51
    2      2.396    male       fs   75
    3      2.838  female       ff   68
    4      2.956    male       fs   29
    5      4.216  female       ff   28
    6      3.620  female       ss   56
    7      2.889  female       ff   38
    8      3.550  female       fs   32
    9      3.105    male       fs   61
    10     4.556  female       fs   20
    11     3.087  female       fs   57
    12     4.939    male       ff   71
    13     3.486    male       ff   21
    14     3.079  female       ss   43
    15     2.649    male       fs   62
    16     1.943  female       fs   54
    17     4.198  female       ff   45
    18     2.473  female       ff   27
    19     2.033  female       ff   66
    20     2.200  female       fs   74
    21     2.157  female       fs   19
    22     2.801    male       ss   20
    23     3.421    male       ss   75
    24     1.811  female       ff   68
    25     4.281  female       fs   25
    26     4.772  female       fs   38
    27     3.586  female       ss   18
    28     3.944  female       ff   49
    29     2.669  female       ss   18
    30     3.050  female       ss   34
    31     4.275    male       ss   49
    32     2.963  female       ss   42
    33     3.236  female       ss   25
    34     3.673  female       ss   55
    35     3.110    male       ss   73

    We want to test that whether the mean values of Activity are different between male and female, and between ff, fs and ss, with *Age* being controlled.

    >>> summary, result = bs.two_way_ancova(data=data, variable="Activity", between_1="Sex", between_2="Genotype", covariable="Age")
    >>> summary
          Sex Genotype  Count  Mean (Activity)  Std. (Activity)  Mean (Age)  Std. (Age)
    1    male       ff      4          3.14800         1.374512      53.000   23.151674
    2    male       fs      4          2.77650         0.316843      56.750   19.568257
    3    male       ss      4          3.40175         0.634811      54.250   25.708300
    4  female       ff      8          3.05025         0.959903      48.625   17.204132
    5  female       fs      8          3.31825         1.144539      39.875   19.910066
    6  female       ss      8          3.23450         0.361775      36.375   15.202796

    The mean values of *Activity* and *Age* in each combination of groups are given.

    >>> result
                    Sum Square  D.F.  F Statistic   p-value      
    Sex               0.018057     1     0.023349  0.879612  <NA>
    Genotype          0.113591     2     0.073441  0.929363  <NA>
    Sex : Genotype    0.727884     2     0.470606  0.629311  <NA>
    Age               1.286714     1     1.663822  0.207280  <NA>
    Residual         22.427109    29          NaN       NaN  <NA>

    After controlling *Age*, the p-value of *Sex* > 0.05, so *Activity* are not different between the two *Sex*. The p-value of *Genotype* > 0.05, so *Activity* are not different between the three *Genotype*. The p-value of interaction > 0.05, so there is no interaction between *Sex* and *Genotype*. 

    '''

    data = data[list({variable, between_1, between_2, covariable})].dropna()
    _process(data, num=[variable, covariable], cat=[between_1, between_2])

    if str(data[variable].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between_1].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between_1))
    if data[between_2].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between_2))
    if str(data[covariable].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(covariable))

    group_1 = data[between_1].dropna().unique()
    group_2 = data[between_2].dropna().unique()

    summary = pd.DataFrame()


    summary = pd.DataFrame()

    for x in group_1:
        for y in group_2:
            n = _CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][[variable, covariable]].dropna()[variable].count())
            mean_1 = _CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][[variable, covariable]].dropna()[variable].mean())
            std_1 = _CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][[variable, covariable]].dropna()[variable].std())
            mean_2 = _CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][[variable, covariable]].dropna()[covariable].mean())
            std_2 = _CC(lambda: data[(data[between_1]==x) & (data[between_2]==y)][[variable, covariable]].dropna()[covariable].std())
            temp = pd.DataFrame(
                {
                    "{}".format(between_1): _CC(lambda: x),
                    "{}".format(between_2): _CC(lambda: y),
                    "Count": _CC(lambda: n),
                    "Mean ({})".format(variable): _CC(lambda: mean_1),
                    "Std. ({})".format(variable): _CC(lambda: std_1),
                    "Mean ({})".format(covariable): _CC(lambda: mean_2),
                    "Std. ({})".format(covariable): _CC(lambda: std_2),
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
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result

def multivariate_anova(data, variable, between):
    '''
    Test whether the mean values of several variables are different between several groups.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two numeric columns and one categorical column.
    variable : :py:class:`list`
        The list of numeric variables that we want to calculate mean values of.
    between : :py:class:`str`
        The categorical variable that specifies which group the samples belong to.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The mean values and standard deviations of each numeric variable in each group.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, Pillai's Trace, F statistic, and p-value of the test.

    See also
    --------
    one_way_anova : Test whether the mean values of a variable are different between groups.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("multivariate_anova.csv")
    >>> data
         sepal_length  sepal_width    species
    0             5.1          3.5     setosa
    1             4.9          3.0     setosa
    2             4.7          3.2     setosa
    3             4.6          3.1     setosa
    4             5.0          3.6     setosa
    ..            ...          ...        ...
    145           6.7          3.0  virginica
    146           6.3          2.5  virginica
    147           6.5          3.0  virginica
    148           6.2          3.4  virginica
    149           5.9          3.0  virginica

    We want to test whether the mean values of *sepal_length* and *sepal_width* in each *species* are different.

    >>> summary, result = bs.multivariate_anova(data=data, variable=["sepal_length", "sepal_width"], between="species")
    >>> summary
          species  Mean (sepal_length)  Std. (sepal_length)  Mean (sepal_width)  Std. (sepal_width)
    1      setosa                5.006             0.352490               3.428            0.379064
    2  versicolor                5.936             0.516171               2.770            0.313798
    3   virginica                6.588             0.635880               2.974            0.322497

    The mean values of *sepal_length* and *sepal_width* in each *species* are given.

    >>> result
             D.F.  Pillai's Trace  F Statistic       p-value     
    species     2        0.945314     65.87798  9.902977e-40  ***

    The p-value < 0.001, so the mean values of *sepal_length* and *sepal_width* in each group are significantly different.

    '''

    data = data[list(set(variable + [between]))].dropna()
    _process(data, num=variable, cat=[between])

    for var in variable:
        if str(data[var].dtypes) not in ("float64", "Int64"):
            raise Warning("The column '{}' must be numeric".format(var))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))

    group = data[between].dropna().unique().tolist()

    summary = pd.DataFrame({between:group})
    for var in variable:
        mean = []
        std = []
        for x in group:
            mean.append(_CC(lambda: data[data[between]==x][var].dropna().mean()))
            std.append(_CC(lambda: data[data[between]==x][var].dropna().std()))
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
            "D.F." : _CC(lambda: len(group)-1) ,
            "Pillai's Trace" : _CC(lambda: table.iloc[1][0]) ,
            "F Statistic" : _CC(lambda: table.iloc[1][3]) ,
            "p-value" : _CC(lambda: table.iloc[1][4])
        }, index=[between]
    )
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result

def repeated_measures_anova(data, variable, between, subject):
    '''
    Test whether the mean values of a variable are different between several groups on repeated measured data.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and one categorical column, as well as a column specifying the subjects.
    variable : :py:class:`str`
        The numeric variable that we want to calculate mean values of.
    between : :py:class:`str`
        The categorical variable that specifies which group the samples belong to.
    subject : :py:class:`str`
        The variable that specifies the subject ID. Samples measured on the same subject should have the same ID.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The counts, mean values, standard deviations, and confidence intervals of each group.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, sum of squares, mean of squares, F statistic, and p-value of the test.

    See also
    --------
    one_way_anova : Test whether the mean values of a variable are different between groups.
    friedman_test : The non-parametric version of repeated measure ANOVA.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("repeated_measures_anova.csv")
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

    We want to test whether the mean values of *response* in each *drug* are different, when the samples are repeatedly measured on the four *patient*.

    >>> summary, result = bs.repeated_measures_anova(data=data, variable="response", between="drug", subject="patient")
    >>> summary
      drug  Count  Mean  Std. Deviation  95% CI: Lower  95% CI: Upper
    1    A      5  26.4        8.763561      15.518602      37.281398
    2    B      5  25.6        6.542171      17.476822      33.723178
    3    C      5  15.6        3.847077      10.823223      20.376777
    4    D      5  32.0        8.000000      22.066688      41.933312

    The mean values of *response* and their 95% confidence intervals in each group are given.

    >>> result
              D.F.  Sum Square  Mean Square  F Statistic  p-value     
    drug         3       698.2   232.733333    24.758865  0.00002  ***
    Residual    12       112.8     9.400000          NaN      NaN  NaN

    The p-value < 0.001, so the mean values of *response* in each group are significantly different.

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
        n = _CC(lambda: data[data[between]==x][variable].dropna().count())
        mean = _CC(lambda: data[data[between]==x][variable].dropna().mean())
        std = _CC(lambda: data[data[between]==x][variable].dropna().std())
        sem = _CC(lambda: data[data[between]==x][variable].dropna().sem())
        temp = pd.DataFrame(
            {
                "{}".format(between): _CC(lambda: x),
                "Count": _CC(lambda: n),
                "Mean": _CC(lambda: mean),
                "Std. Deviation": _CC(lambda: std),
                "95% CI: Lower" : _CC(lambda: st.t.ppf(0.025, n-1, mean, sem)) ,
                "95% CI: Upper" : _CC(lambda: st.t.ppf(0.975, n-1, mean, sem)) ,
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

    df_1 = _CC(lambda: anova_1.iloc[0][0])
    df_2 = _CC(lambda: df_1 * anova_2.iloc[0][0])
    SS_1 = _CC(lambda: anova_1.iloc[0][1])
    SS_2 = _CC(lambda: anova_2.iloc[1][1] - SS_1)
    MS_1 = _CC(lambda: SS_1 / df_1)
    MS_2 = _CC(lambda: SS_2 / df_2)
    F = _CC(lambda: MS_1 / MS_2)
    p = _CC(lambda: 1 - st.f.cdf(F, df_1, df_2))

    result = pd.DataFrame(
        {
            "D.F." : [df_1, df_2] ,
            "Sum Square" : [SS_1, SS_2] ,
            "Mean Square" : [MS_1, MS_2] ,
            "F Statistic" : [F, None] ,
            "p-value" : [p, None]
        }, index = [between, "Residual"]
    )
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result

