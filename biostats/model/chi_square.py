import numpy as np
import pandas as pd
from scipy import stats as st

from biostats.model.util import _CC, _process, _add_p

def chi_square_test(data, variable_1, variable_2, kind="count"):
    '''
    Test whether there is an association between two categorical variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two categorical columns.
    variable_1 : :py:class:`str`
        The first categorical variable. Maximum 20 groups.
    variable_2 : :py:class:`str`
        The second categorical variable. Maximum 20 groups. Switching the two variables will not change the result of chi-square test.
    kind : :py:class:`str`
        The way to summarize the contingency table.
        
        * "count" : Count the frequencies of occurance.
        * "vertical" : Calculate proportions vertically, so that the sum of each column equals 1.
        * "horizontal" : Calculate proportions horizontally, so that the sum of each row equals 1.
        * "overall" : Calculate overall proportions, so that the sum of the whole table equals 1.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The contingency table of the two categorical variables.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, chi-square statistic, and p-value of the test.

    See also
    --------
    fisher_exact_test : The exact version of chi-square test.
    chi_square_test_fit : Test the difference between the observed and expected proportion of a variable.
    mantel_haenszel_test : Test the association between two categorical variables in stratified data.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("chi_square_test.csv")
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

    We want to test whether there is an association between *Genotype* and *Health*.

    >>> summary, result = bs.chi_square_test(data=data, variable_1="Genotype", variable_2="Health", kind="horizontal")
    >>> summary
              disease  no_disease
    del-del  0.814159    0.185841
    ins-del  0.792276    0.207724
    ins-ins  0.750698    0.249302

    The proportions of *disease* in different *Genotype* are given.

    >>> result
            D.F.  Chi Square   p-value   
    Normal     2    7.259386  0.026524  *

    The p-value < 0.05, so there is a significant association between *Genotype* and *Health*. That is, the proportions of *disease* are different between the three *Genotype*.

    '''
    
    data = data[list({variable_1, variable_2})].dropna()
    _process(data, cat=[variable_1, variable_2])

    if data[variable_1].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_1))
    if data[variable_2].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_2))

    summary = pd.crosstab(index=data[variable_1], columns=data[variable_2])
    summary.index.name = None
    summary.columns.name = None

    obs = summary.values.tolist()

    if kind == "vertical":
        col_sum = _CC(lambda: summary.sum(axis=0))
        for i in range(summary.shape[0]):
            for j in range(summary.shape[1]):
                summary.iat[i,j] = _CC(lambda: summary.iat[i,j] / col_sum[j])

    if kind == "horizontal":
        col_sum = _CC(lambda: summary.sum(axis=1))
        for i in range(summary.shape[0]):
            for j in range(summary.shape[1]):
                summary.iat[i,j] = _CC(lambda: summary.iat[i,j] / col_sum[i])

    if kind == "overall":
        _sum = _CC(lambda: summary.to_numpy().sum())
        for i in range(summary.shape[0]):
            for j in range(summary.shape[1]):
                summary.iat[i,j] = _CC(lambda: summary.iat[i,j] / _sum)

    rr = _CC(lambda: len(obs))
    cc = _CC(lambda: len(obs[0]))
    r_sum = []
    c_sum = []
    _sum = 0

    for i in range(rr):
        temp = 0
        for j in range(cc):
            temp = _CC(lambda: temp + obs[i][j])
        r_sum.append(temp)
    for j in range(cc):
        temp = 0
        for i in range(rr):
            temp = _CC(lambda: temp + obs[i][j])
        c_sum.append(temp)
    for i in range(rr):
        _sum = _CC(lambda: _sum + r_sum[i])
    
    exp = []

    for i in range(rr):
        temp = []
        for j in range(cc):
            temp.append(_CC(lambda: r_sum[i] * c_sum[j] / _sum))
        exp.append(temp)
    
    chi2 = 0
    for i in range(rr):
        for j in range(cc):
            chi2 = _CC(lambda: chi2 + (obs[i][j]-exp[i][j]) ** 2 / exp[i][j])
    
    p = _CC(lambda: 1 - st.chi2.cdf(chi2, (rr-1)*(cc-1)))

    result = pd.DataFrame(
        {
            "D.F.": _CC(lambda: (rr-1)*(cc-1)),
            "Chi Square": _CC(lambda: chi2),
            "p-value": _CC(lambda: p)
        }, index=["Normal"]
    )

    if summary.shape == (2,2):
        chi2 = 0
        for i in range(rr):
            for j in range(cc):
                chi2 = _CC(lambda: chi2 + (abs(obs[i][j]-exp[i][j])-0.5) ** 2 / exp[i][j])
        
        p = _CC(lambda: 1 - st.chi2.cdf(chi2, (rr-1)*(cc-1)))

        result2 = pd.DataFrame(
            {
            "D.F.": _CC(lambda: (rr-1)*(cc-1)),
            "Chi Square": _CC(lambda: chi2),
            "p-value": _CC(lambda: p)
            }, index=["Corrected"]
        )
        result = pd.concat([result, result2], axis=0)
    
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result

def chi_square_test_fit(data, variable, expect):
    '''
    Test whether the proportion of a categorical variable is different from the expected proportion.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one categorical column.
    variable : :py:class:`str`
        The categorical variable that we want to calculate the proportion of. Maximum 20 groups.
    expect : :py:class:`dict`
        The expected proportions of each group. The sum of the proportions will be automatically normalized to 1.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The observed counts and proportions of each group, and the expected counts and proportions of each group.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, chi-square statistic, and p-value of the test.

    See also
    --------
    binomial_test : The exact version of chi-square test (fit).
    chi_square_test : Test the association between two categorical variables.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("chi_square_test_fit.csv")
    >>> data
            Canopy
    0      Douglas
    1    Ponderosa
    2    Ponderosa
    3    Ponderosa
    4      Douglas
    ..         ...
    151    Douglas
    152    Douglas
    153  Ponderosa
    154    Douglas
    155    Douglas

    We want to test whether the proportions of each *Canopy* are different from the expected proportions.

    >>> summary, result = bs.chi_square_test_fit(data=data, variable="Canopy", expect={"Douglas":0.54, "Ponderosa":0.40, "Grand":0.05, "Western":0.01})
    >>> summary
               Observe  Prop.(Obs.)  Expect  Prop.(Exp.)
    Douglas         70     0.448718   84.24         0.54
    Ponderosa       79     0.506410   62.40         0.40
    Western          4     0.025641    1.56         0.01
    Grand            3     0.019231    7.80         0.05

    The observed and expected counts and proportions of each group are given.

    >>> result
            D.F.  Chi Square   p-value    
    Normal     3   13.593424  0.003514  **

    The p-value < 0.01, so the observed proportions are significantly different from the expected proportions.

    '''
    
    data = data[[variable]].dropna()
    _process(data, cat=[variable])

    if data[variable].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable))

    cat = data.groupby(variable, sort=False)[variable].groups.keys()
    obs = []
    exp = []
    pro_o = []
    pro_e = []
    exp_sum = sum(list(expect.values()))
    for var in cat:
        obs_val = _CC(lambda: data[variable].value_counts()[var])
        obs.append(_CC(lambda: obs_val))
        pro_o.append(_CC(lambda: obs_val / len(data)))
        exp.append(_CC(lambda: expect[var] * len(data) / exp_sum))
        pro_e.append(_CC(lambda: expect[var] / exp_sum))

    summary = pd.DataFrame(
        {
            "Observe" : _CC(lambda: obs),
            "Prop.(Obs.)" : _CC(lambda: pro_o),
            "Expect"  : _CC(lambda: exp),
            "Prop.(Exp.)" : _CC(lambda: pro_e),
        }, index=cat
    )

    dim = _CC(lambda: len(obs))
    chi2 = 0
    for i in range(dim):
        chi2 = _CC(lambda: chi2 + (obs[i]-exp[i]) * (obs[i]-exp[i]) / exp[i])
    p = _CC(lambda: 1 - st.chi2.cdf(chi2, dim-1))
    result = pd.DataFrame(
        {
            "D.F.": _CC(lambda: dim-1),
            "Chi Square": _CC(lambda: chi2),
            "p-value": _CC(lambda: p)
        }, index=["Normal"]
    )

    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result

def mcnemar_test(data, variable_1, variable_2, pair):
    '''
    Test whether the proportions of a categorical variable are different in two paired groups.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two categorical columns, and a column specifying the pairs.
    variable_1 : :py:class:`str`
        The categorical variable that specifies which group the samples belong to. Maximum 20 groups. The most frequently appearing two groups will be chosen automatically.
    variable_2 : :py:class:`str`
        The categorical variable that we want to calculate proportions of. Maximum 20 groups. The most frequently appearing two groups will be chosen automatically.
    pair : :py:class:`str`
        The variable that specifies the pair ID. Samples in the same pair should have the same ID. Maximum 2000 pairs.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The contingency table of the two categorical variables with matched pairs as the unit.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, chi-square statistic, and p-value of the test (both normal and corrected).

    See also
    --------
    mcnemar_exact_test : The exact version of McNemar's test,
    chi_square_test : Test the association between two categorical variables.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("mcnemar_test.csv")
    >>> data
        Treatment       Result   ID
    0      before      support    1
    1      before      support    2
    2      before      support    3
    3      before      support    4
    4      before      support    5
    ..        ...          ...  ...
    195     after  not_support   96
    196     after  not_support   97
    197     after  not_support   98
    198     after  not_support   99
    199     after  not_support  100

    We want to test whether the proportions of *Result* are different between the two *Treatment*, where each *before* is paired with a *after*.

    >>> summary, result = bs.mcnemar_test(data=data, variable_1="Treatment", variable_2="Result", pair="ID")
    >>> summary
                          after : support  after : not_support
    before : support                   30                   12
    before : not_support               40                   18

    The contingency table of *Treatment* and *Result* where the counting unit is the matched pair.

    >>> result
               D.F.  Chi Square   p-value     
    Normal        1   15.076923  0.000103  ***
    Corrected     1   14.019231  0.000181  ***

    The p-value < 0.001, so there is a significant difference between the proportions of *Result* under the two *Treatment*.

    '''

    data = data[list({variable_1, variable_2, pair})].dropna()
    _process(data, cat=[variable_1, variable_2, pair])

    if data[variable_1].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_1))
    if data[variable_2].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_2))
    if data[pair].nunique() > 2000:
        raise Warning("The nmuber of classes in column '{}' cannot > 2000.".format(pair))

    grp_1 = data[variable_1].value_counts()[:2].index.tolist()
    grp_2 = data[variable_2].value_counts()[:2].index.tolist()

    data = data[data[variable_1].isin(grp_1)]
    data = data[data[variable_2].isin(grp_2)]

    cross = pd.crosstab(index=data[pair], columns=data[variable_1])
    for col in cross:
        cross = cross.drop(cross[cross[col] != 1].index)
    sub = cross.index.values.tolist()
    data = data[data[pair].isin(sub)]

    _dat = pd.DataFrame(
        {
            "fst" : data[data[variable_1]==grp_1[0]].sort_values(by=[pair])[variable_2].tolist() ,
            "snd" : data[data[variable_1]==grp_1[1]].sort_values(by=[pair])[variable_2].tolist()
        }
    )

    a = _CC(lambda: _dat[(_dat["fst"]==grp_2[0]) & (_dat["snd"]==grp_2[0])]["fst"].count())
    b = _CC(lambda: _dat[(_dat["fst"]==grp_2[0]) & (_dat["snd"]==grp_2[1])]["fst"].count())
    c = _CC(lambda: _dat[(_dat["fst"]==grp_2[1]) & (_dat["snd"]==grp_2[0])]["fst"].count())
    d = _CC(lambda: _dat[(_dat["fst"]==grp_2[1]) & (_dat["snd"]==grp_2[1])]["fst"].count())

    summary = pd.DataFrame(
        {
            "{} : {}".format(grp_1[1], grp_2[0]) : [a, c] ,
            "{} : {}".format(grp_1[1], grp_2[1]) : [b, d] ,
        }, index=["{} : {}".format(grp_1[0], grp_2[0]), "{} : {}".format(grp_1[0], grp_2[1])]
    )

    chi2 = _CC(lambda: (b - c) ** 2 / (b + c))
    chi2_ = _CC(lambda: (abs(b-c) - 1) ** 2 / (b + c))
    p = _CC(lambda: 1 - st.chi2.cdf(chi2, 1))
    p_ = _CC(lambda: 1 - st.chi2.cdf(chi2_, 1))

    result = pd.DataFrame(
        {
            "D.F." : [1, 1] ,
            "Chi Square" : [chi2, chi2_] ,
            "p-value" : [p, p_]
        }, index=["Normal", "Corrected"]
    )
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result


def mantel_haenszel_test(data, variable_1, variable_2, stratum):
    '''
    Test whether there is an association between two categorical variables in stratified data.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least three categorical columns.
    variable_1 : :py:class:`str`
        The first categorical variable. Maximum 20 groups.
    variable_2 : :py:class:`str`
        The second categorical variable. Maximum 20 groups. Switching the two variables will not change the result.
    stratum : :py:class:`str`
        The categorical variable that specifies which stratum the samples belong to. Maximum 30 strata.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The contingency table of the two categorical variables in each stratum.
    result : :py:class:`pandas.DataFrame`
        The degree of freedom, chi-square statistic, and p-value of the test.

    See also
    --------
    chi_square_test : Test the association between two categorical variables.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("mantel_haenszel_test.csv")
    >>> data
        Treatment Revascularization  Study
    0      Niacin               Yes   FATS
    1      Niacin               Yes   FATS
    2      Niacin                No   FATS
    3      Niacin                No   FATS
    4      Niacin                No   FATS
    ..        ...               ...    ...
    669   Placebo                No  CLAS1
    670   Placebo                No  CLAS1
    671   Placebo                No  CLAS1
    672   Placebo                No  CLAS1
    673   Placebo                No  CLAS1

    We want to test whether there is an association between *Treatment* and *Revascularization*, with the data including the five *Study*.

    >>> summary, result = bs.mantel_haenszel_test(data=data, variable_1="Treatment", variable_2="Revascularization", stratum="Study")
    >>> summary
                         No   Yes
    FATS       Niacin    46     2
              Placebo    41    11
                       <NA>  <NA>
    AFREGS     Niacin    67     4
              Placebo    60    12
                       <NA>  <NA>
    ARBITER2   Niacin    86     1
              Placebo    76     4
                       <NA>  <NA>
    HATS       Niacin    37     1
              Placebo    32     6
                       <NA>  <NA>
    CLAS1      Niacin    92     2
              Placebo    93     1
                       <NA>  <NA>

    The contingency tables of *Treatment* and *Revascularization* in the five *Study*.

    >>> result
            D.F.  Chi Square   p-value     
    Normal     1   12.745723  0.000357  ***

    The p-value < 0.001, so there is a significant association between *Treatment* and *Revascularization* in the stratified data.

    '''

    data = data[list({variable_1, variable_2, stratum})].dropna()
    _process(data, cat=[variable_1, variable_2, stratum])
    
    if data[variable_1].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_1))
    if data[variable_2].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_2))
    if data[stratum].nunique() > 30:
        raise Warning("The nmuber of classes in column '{}' cannot > 30.".format(stratum))

    study = data[stratum].dropna().unique()
    grp_1 = data[variable_1].value_counts()[:2].index.tolist()
    grp_2 = data[variable_2].value_counts()[:2].index.tolist()

    summary = pd.DataFrame(columns=["", grp_2[0], grp_2[1]])

    O, V, E = 0, 0 ,0

    for stu in study:
        part = data.loc[data[stratum]==stu]
        a = _CC(lambda: part[(part[variable_1]==grp_1[0]) & (part[variable_2]==grp_2[0])][stratum].count())
        b = _CC(lambda: part[(part[variable_1]==grp_1[0]) & (part[variable_2]==grp_2[1])][stratum].count())
        c = _CC(lambda: part[(part[variable_1]==grp_1[1]) & (part[variable_2]==grp_2[0])][stratum].count())
        d = _CC(lambda: part[(part[variable_1]==grp_1[1]) & (part[variable_2]==grp_2[1])][stratum].count())
        n = _CC(lambda: a + b + c + d)
        temp = pd.DataFrame(
            {
                "" : [grp_1[0], grp_1[1], ""] ,
                grp_2[0] : [a, c, np.nan] ,
                grp_2[1] : [b, d, np.nan]
            }, index=[stu, "", ""]
        )
        summary = pd.concat([summary, temp])

        O = _CC(lambda: O + a)
        E = _CC(lambda: E + (a + b) * (a + c) / n)
        V = _CC(lambda: V + (a + b) * (c + d) * (a + c) * (b + d) / (n**3 - n**2))
    
    chi2 = _CC(lambda: (abs(O-E) - 0.5) ** 2 / V)
    p = _CC(lambda: 1 - st.chi2.cdf(chi2, 1))

    result = pd.DataFrame(
        {
            "D.F.": 1,
            "Chi Square": _CC(lambda: chi2),
            "p-value": _CC(lambda: p)
        }, index=["Normal"]
    )
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result
