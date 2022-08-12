import pandas as pd
import numpy as np
from scipy import stats as st
from statsmodels.stats.proportion import proportion_confint

from biostats.model.util import _CC, _process, _add_p

def numeric(data, variable):
    '''
    Compute descriptive statistics of numeric variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column.
    variable : :py:class:`list`
        The list of numeric variables to be analyzed.

    Returns
    -------
    result : :py:class:`pandas.DataFrame`
        The count, arithmetic mean, median, geometric mean, harmonic mean, mode, / sample variance, sample standard deviation, coefficient of variation, population variance, population standard deviation, / minimum, 25% percentile, 50% percentile, 75% percentile, maximum, range, interquartile range, / standard error, two-sided 95% confidence interval (lower and upper limit), and one-sided 95% confidence interval (lower and upper limit) of each variable.

    See also
    --------
    numeric_grouped : Compute descriptive statistics of a numeric variable in different groups.
    one_sample_t_test : Test whether the mean value of a variable is different from the expected value.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("numeric.csv")
    >>> data
       Fish  Crab  Temperature
    0    76   123         25.7
    1   102   265         20.1
    2    12    35          4.2
    3    39    86         11.4
    4    55   140         31.2
    5    93   315         21.0
    6    98   279         17.8
    7    53   120         13.3
    8   102   312         18.5

    We want to compute descriptive statistics of the three variables.

    >>> result = bs.numeric(data=data, variable=["Fish", "Crab", "Temperature"])
    >>> result
                                      Fish          Crab  Temperature
    Count                         9.000000      9.000000     9.000000
    Mean                         70.000000    186.111111    18.133333
    Median                       76.000000    140.000000    18.500000
    Geometric Mean               59.835149    152.721285    16.057497
    Harmonic Mean                45.057085    116.064406    13.243700
    Mode                        102.000000     35.000000     4.200000
                                       NaN           NaN          NaN
    Variance                   1029.500000  11331.111111    62.895000
    Std. Deviation               32.085822    106.447692     7.930637
    Coef. Variation               0.458369      0.571958     0.437351
    (Population) Variance       915.111111  10072.098765    55.906667
    (Population) Std.Dev         30.250803    100.359846     7.477076
                                       NaN           NaN          NaN
    Minimum                      12.000000     35.000000     4.200000
    25% Percentile               53.000000    120.000000    13.300000
    50% Percentile               76.000000    140.000000    18.500000
    75% Percentile               98.000000    279.000000    21.000000
    Maximum                     102.000000    315.000000    31.200000
    Range                        90.000000    280.000000    27.000000
    Interquartile Range          45.000000    159.000000     7.700000
                                       NaN           NaN          NaN
    Std. Error                   10.695274     35.482564     2.643546
    95% CI: Lower                45.336654    104.288172    12.037306
    95% CI: Upper                94.663346    267.934050    24.229360
    (One-Sided) 95% CI: Lower    50.111624    120.129579    13.217533
    (One-Sided) 95% CI: Upper    89.888376    252.092643    23.049133

    Descriptive statistics of the three variables are computed.

    '''

    data = data[list(set(variable))].dropna(how='all')
    _process(data, num=variable)

    for var in variable:
        if str(data[var].dtypes) not in ("float64", "Int64"):
            print(str(data[var].dtypes))
            raise Warning("The column '{}' must be numeric".format(var))

    index = ["Count", "Mean", "Median", "Geometric Mean", "Harmonic Mean", "Mode"]
    index += ["", "Variance", "Std. Deviation", "Coef. Variation", "(Population) Variance", "(Population) Std.Dev"]
    index += ["", "Minimum", "25% Percentile", "50% Percentile", "75% Percentile", "Maximum", "Range", "Interquartile Range"]
    index += ["", "Std. Error", "95% CI: Lower", "95% CI: Upper", "(One-Sided) 95% CI: Lower", "(One-Sided) 95% CI: Upper"]
    result = pd.DataFrame(index=index)

    for var in variable:
        result[var] = [
            _CC(data[var].count) ,
            _CC(st.tmean, data[var].dropna()) ,
            _CC(np.median, data[var].dropna()) ,
            _CC(st.gmean, data[var].dropna()) ,
            _CC(st.hmean, data[var].dropna()) ,
            _CC(lambda a: st.mode(a)[0][0], data[var].dropna()) ,
            np.nan ,
            _CC(st.tvar, data[var].dropna()) ,
            _CC(st.tstd, data[var].dropna()) ,
            _CC(lambda a: st.tstd(a)/st.tmean(a), data[var].dropna()) ,
            _CC(np.var, data[var].dropna()) ,
            _CC(np.std, data[var].dropna()) ,
            np.nan ,
            _CC(np.percentile, data[var].dropna(), 0) ,
            _CC(np.percentile, data[var].dropna(), 25) ,
            _CC(np.percentile, data[var].dropna(), 50) ,
            _CC(np.percentile, data[var].dropna(), 75) ,
            _CC(np.percentile, data[var].dropna(), 100) ,
            _CC(lambda a: np.percentile(a,100)-np.percentile(a,0), data[var].dropna()) ,
            _CC(lambda a: np.percentile(a,75)-np.percentile(a,25), data[var].dropna()) ,
            np.nan ,
            _CC(st.tsem, data[var].dropna()) ,
            _CC(lambda a: st.t.ppf(0.025, a.count()-1, st.tmean(a), st.tsem(a)), data[var].dropna()) ,
            _CC(lambda a: st.t.ppf(0.975, a.count()-1, st.tmean(a), st.tsem(a)), data[var].dropna()) ,
            _CC(lambda a: st.t.ppf(0.050, a.count()-1, st.tmean(a), st.tsem(a)), data[var].dropna()) ,
            _CC(lambda a: st.t.ppf(0.950, a.count()-1, st.tmean(a), st.tsem(a)), data[var].dropna()) ,
        ]

    _process(result)

    return result


def numeric_grouped(data, variable, group):
    '''
    Compute descriptive statistics of a numeric variable in different groups.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and one categorical column.
    variable : :py:class:`str`
        The numeric variable that we want to analyze.
    group : :py:class:`str`
        The categorical variable that specifies which group the samples belong to.

    Returns
    -------
    result : :py:class:`pandas.DataFrame`
        The count, arithmetic mean, median, geometric mean, harmonic mean, mode, / sample variance, sample standard deviation, coefficient of variation, population variance, population standard deviation, / minimum, 25% percentile, 50% percentile, 75% percentile, maximum, range, interquartile range, / standard error, two-sided 95% confidence interval (lower and upper limit), and one-sided 95% confidence interval (lower and upper limit) of the variable in each group.

    See also
    --------
    numeric : Compute descriptive statistics of numeric variables.
    one_way_anova : Test whether the mean values of a variable are different between several groups.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("numeric_grouped.csv")
    >>> data
        Count  Animal
    0      76    Fish
    1     102    Fish
    2      12    Fish
    3      39    Fish
    4      55    Fish
    5      93    Fish
    6      98    Fish
    7      53    Fish
    8     102    Fish
    9      28  Insect
    10     85  Insect
    11     17  Insect
    12     20  Insect
    13     33  Insect
    14     75  Insect
    15     78  Insect
    16     25  Insect
    17     87  Insect

    We want to compute descriptive statistics of *Count* in the two *Animal*.

    >>> result = bs.numeric_grouped(data=data, variable="Count", group="Animal")
    >>> result
                                     Fish      Insect
    Count                        9.000000    9.000000
    Mean                        70.000000   49.777778
    Median                      76.000000   33.000000
    Geometric Mean              59.835149   41.169549
    Harmonic Mean               45.057085   34.058186
    Mode                       102.000000   17.000000
                                      NaN         NaN
    Variance                  1029.500000  923.694444
    Std. Deviation              32.085822   30.392342
    Coef. Variation              0.458369    0.610560
    (Population) Variance      915.111111  821.061728
    (Population) Std.Dev        30.250803   28.654175
                                      NaN         NaN
    Minimum                     12.000000   17.000000
    25% Percentile              53.000000   25.000000
    50% Percentile              76.000000   33.000000
    75% Percentile              98.000000   78.000000
    Maximum                    102.000000   87.000000
    Range                       90.000000   70.000000
    Interquartile Range         45.000000   53.000000
                                      NaN         NaN
    Std. Error                  10.695274   10.130781
    95% CI: Lower               45.336654   26.416156
    95% CI: Upper               94.663346   73.139400
    (One-Tail) 95% CI: Lower    50.111624   30.939105
    (One-Tail) 95% CI: Upper    89.888376   68.616451

    Descriptive statistics of *Count* in the two *Animal* are computed.

    '''

    data = data[list({variable, group})].dropna()
    _process(data, num=[variable], cat=[group])

    if str(data[variable].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[group].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(group))

    index = ["Count", "Mean", "Median", "Geometric Mean", "Harmonic Mean", "Mode"]
    index += ["", "Variance", "Std. Deviation", "Coef. Variation", "(Population) Variance", "(Population) Std.Dev"]
    index += ["", "Minimum", "25% Percentile", "50% Percentile", "75% Percentile", "Maximum", "Range", "Interquartile Range"]
    index += ["", "Std. Error", "95% CI: Lower", "95% CI: Upper", "(One-Tail) 95% CI: Lower", "(One-Tail) 95% CI: Upper"]
    result = pd.DataFrame(index=index)

    for cat in data[group].dropna().unique():
        result[cat] = [
            _CC(data[data[group]==cat][variable].count) ,
            _CC(st.tmean, data[data[group]==cat][variable].dropna()) ,
            _CC(np.median, data[data[group]==cat][variable].dropna()) ,
            _CC(st.gmean, data[data[group]==cat][variable].dropna()) ,
            _CC(st.hmean, data[data[group]==cat][variable].dropna()) ,
            _CC(lambda a: st.mode(a)[0][0], data[data[group]==cat][variable].dropna()) ,
            np.nan ,
            _CC(st.tvar, data[data[group]==cat][variable].dropna()) ,
            _CC(st.tstd, data[data[group]==cat][variable].dropna()) ,
            _CC(lambda a: st.tstd(a)/st.tmean(a), data[data[group]==cat][variable].dropna()) ,
            _CC(np.var, data[data[group]==cat][variable].dropna()) ,
            _CC(np.std, data[data[group]==cat][variable].dropna()) ,
            np.nan ,
            _CC(np.percentile, data[data[group]==cat][variable].dropna(), 0) ,
            _CC(np.percentile, data[data[group]==cat][variable].dropna(), 25) ,
            _CC(np.percentile, data[data[group]==cat][variable].dropna(), 50) ,
            _CC(np.percentile, data[data[group]==cat][variable].dropna(), 75) ,
            _CC(np.percentile, data[data[group]==cat][variable].dropna(), 100) ,
            _CC(lambda a: np.percentile(a,100)-np.percentile(a,0), data[data[group]==cat][variable].dropna()) ,
            _CC(lambda a: np.percentile(a,75)-np.percentile(a,25), data[data[group]==cat][variable].dropna()) ,
            np.nan ,
            _CC(st.tsem, data[data[group]==cat][variable].dropna()) ,
            _CC(lambda a: st.t.ppf(0.025, a.count()-1, st.tmean(a), st.tsem(a)), data[data[group]==cat][variable].dropna()) ,
            _CC(lambda a: st.t.ppf(0.975, a.count()-1, st.tmean(a), st.tsem(a)), data[data[group]==cat][variable].dropna()) ,
            _CC(lambda a: st.t.ppf(0.050, a.count()-1, st.tmean(a), st.tsem(a)), data[data[group]==cat][variable].dropna()) ,
            _CC(lambda a: st.t.ppf(0.950, a.count()-1, st.tmean(a), st.tsem(a)), data[data[group]==cat][variable].dropna()) ,
        ]    

    _process(result)

    return result


def categorical(data, variable):
    '''
    Compute descriptive statistics of a categorical variable.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one categorical column.
    variable : :py:class:`str`
        The categorical variable to be analyzed.

    Returns
    -------
    result : :py:class:`pandas.DataFrame`
        The count, proportion, 95% confidence interval (lower and upper limit) of each group.

    See also
    --------
    contingency : Compute the contingency table of two categorical variables.
    chi_square_test_fit : Test whether the proportion of groups in a categorical variable is different from the expected proportion.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("categorical.csv")
    >>> data
          Color
    0    Yellow
    1      Blue
    2       Red
    3      Blue
    4       Red
    ..      ...
    195  Yellow
    196    Blue
    197     Red
    198    Blue
    199    Blue

    We want to compute descriptive statistics of *Color*.

    >>> result = bs.categorical(data=data, variable="Color")
    >>> result
            Count  Proportion  95% CI: Lower  95% CI: Upper
    Yellow     74       0.370       0.306126       0.438774
    Blue       69       0.345       0.282598       0.413244
    Red        35       0.175       0.128605       0.233644
    Green      22       0.110       0.073772       0.160927

    Descriptive statistics of *Color* are computed.

    '''

    data = data[[variable]].dropna()
    _process(data, cat=[variable])

    if data[variable].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable))

    cat = data.groupby(variable, sort=False)[variable].groups.keys()
    cnt = []
    prop = []
    CI_low = []
    CI_high = []
    for var in cat:
        cnt.append(_CC(lambda: data[variable].value_counts()[var]))
    n = _CC(lambda: sum(cnt))
    for x in cnt:
        prop.append(_CC(lambda: x / n))
        (ci_1, ci_2) = _CC(lambda: proportion_confint(x, n, method="wilson"))
        CI_low.append(ci_1)
        CI_high.append(ci_2)

    result = pd.DataFrame(
        {
            "Count" : _CC(lambda: cnt), 
            "Proportion"  : _CC(lambda: prop),
            "95% CI: Lower" : _CC(lambda: CI_low),
            "95% CI: Upper" : _CC(lambda: CI_high)
        }, index=cat
    )

    _process(result)

    return result


def contingency(data, variable_1, variable_2, kind="count"):
    '''
    Compute the contingency table of two categorical variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two categorical columns.
    variable_1 : :py:class:`str`
        The first categorical variable.
    variable_2 : :py:class:`str`
        The second categorical variable.
    kind : :py:class:`str`
        The way to summarize the contingency table.
        
        * "count" : Count the frequencies of occurance.
        * "vertical" : Calculate proportions vertically, so that the sum of each column equals 1.
        * "horizontal" : Calculate proportions horizontally, so that the sum of each row equals 1.
        * "overall" : Calculate overall proportions, so that the sum of the whole table equals 1.

    Returns
    -------
    result : :py:class:`pandas.DataFrame`
        The contingency table of the two categorical variables.

    See also
    --------
    categorical : Compute descriptive statistics of a categorical variable.
    chi_square_test : Test whether there is an association between two categorical variables.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("contingency.csv")
    >>> data
         Genotype      Health
    0     ins-del     disease
    1     ins-ins     disease
    2     ins-del     disease
    3     ins-ins     disease
    4     ins-del  no_disease
    ...       ...         ...
    2254  ins-ins  no_disease
    2255  ins-del     disease
    2256  ins-del     disease
    2257  ins-ins     disease
    2258  ins-ins  no_disease

    We want to compute the contingency table of *Genotype* and *Health*.

    >>> result = bs.contingency(data=data, variable_1="Genotype", variable_2="Health", kind="count")
    >>> result
             disease  no_disease
    del-del      184          42
    ins-del      759         199
    ins-ins      807         268

    '''

    data = data[list({variable_1, variable_2})].dropna()
    _process(data, cat=[variable_1, variable_2])

    if data[variable_1].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_1))
    if data[variable_2].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_2))
        
    result = pd.crosstab(index=data[variable_1], columns=data[variable_2])
    result.index.name = None
    result.columns.name = None

    if kind == "vertical":
        col_sum = _CC(lambda: result.sum(axis=0))
        for i in range(result.shape[0]):
            for j in range(result.shape[1]):
                result.iat[i,j] = _CC(lambda: result.iat[i,j] / col_sum[j])

    if kind == "horizontal":
        col_sum = _CC(lambda: result.sum(axis=1))
        for i in range(result.shape[0]):
            for j in range(result.shape[1]):
                result.iat[i,j] = _CC(lambda: result.iat[i,j] / col_sum[i])

    if kind == "overall":
        _sum = _CC(lambda: result.to_numpy().sum())
        for i in range(result.shape[0]):
            for j in range(result.shape[1]):
                result.iat[i,j] = _CC(lambda: result.iat[i,j] / _sum)

    _process(result)

    return result