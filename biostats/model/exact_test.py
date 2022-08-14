import numpy as np
import pandas as pd
import math

from biostats.model.util import _CC, _process, _add_p

class binom_exact:

    def __init__(self, table, freqency):
        self.table = table
        self.freq = freqency

    def calc(self):

        self.sum = sum(self.table)

        self.p_part = math.factorial(self.sum)

        self.p_0 = self.multi_nom(self.table)
        self.p = 0
        #self.cnt = 0

        mat = [0] * len(self.table)
        pos = 0

        self.dfs(mat, pos)

        #if self.cnt > 1000000:
        #    return np.NAN

        return self.p

    def dfs(self, mat, pos):

        #self.cnt += 1
        #if self.cnt > 1000000:
        #    return

        mat_new = []
        for x in mat:
            mat_new.append(x)

        if pos == -1:
            temp = self.sum - sum(mat_new)
            if temp <0:
                return
            mat_new[len(mat)-1] = temp

            p_1 = self.multi_nom(mat_new)
            if p_1 <= self.p_0 + 0.000000000000000001:
                self.p += p_1
        else:
            max_ = self.sum - sum(mat_new)
            for k in range(max_+1):
                mat_new[pos] = k
                if pos == len(mat)-2:
                    pos_new = -1
                else:
                    pos_new = pos + 1
                self.dfs(mat_new, pos_new)

    def multi_nom(self, table):
        p = self.p_part
        for i in range(len(table)):
            p *= self.freq[i] ** table[i]
        for x in table:
            p /= math.factorial(x)
        return p

def binomial_test(data, variable, expect):
    '''
    Test whether the proportion of a categorical variable is different from the expected proportion.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one categorical column. Maximum 500 rows.
    variable : :py:class:`str`
        The categorical variable that we want to calculate the proportion of. Maximum 10 groups.
    expect : :py:class:`dict`
        The expected proportions of each group. The sum of the proportions will be automatically normalized to 1.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The observed counts and proportions of each group, and the expected counts and proportions of each group.
    result : :py:class:`pandas.DataFrame`
        The p-value of the test.

    See also
    --------
    chi_square_test_fit : The normal approximation version of binomial test.
    fisher_exact_test : Test the association between two categorical variables.

    Notes
    -----
    .. warning::
        The binomial test calculates the exact p-value by iterating through all the possible distributions, so it may consume lots of time when the size of data is huge. For larger data, :py:func:`chi_square_test_fit` is recommended. 

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("binomial_test.csv")
    >>> data
         Flower
    0    Purple
    1    Purple
    2       Red
    3      Blue
    4     White
    ..      ...
    143  Purple
    144  Purple
    145    Blue
    146     Red
    147    Blue

    We want to test whether the proportion in *Flower* is different from the expected proportions.

    >>> summary, result = bs.binomial_test(data=data, variable="Flower", expect={"Purple":9, "Red":3, "Blue":3, "White":1})
    >>> summary
            Observe  Prop.(Obs.)  Expect  Prop.(Exp.)
    Purple       72     0.486486   83.25       0.5625
    Red          38     0.256757   27.75       0.1875
    Blue         20     0.135135   27.75       0.1875
    White        18     0.121622    9.25       0.0625

    The observed and expected counts and proportions of each group are given.

    >>> result
            p-value    
    Model  0.002255  **

    The p-value < 0.01, so the observed proportions are significantly different from the expected proportions.

    '''

    data = data[[variable]].dropna()
    _process(data, cat=[variable])

    if data[variable].nunique() > 10:
        raise Warning("The nmuber of classes in column '{}' cannot > 10.".format(variable))
    if len(data) > 500:
        raise Warning("The length of data cannot > 500.")

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

    test = binom_exact(obs, pro_e)
    p = _CC(lambda: test.calc())

    result = pd.DataFrame(
        {
            "p-value": _CC(lambda: p)
        }, index=["Model"]
    )

    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result

class fisher_exact:
    
    def __init__(self, table):
        self.table = table

    def calc(self):

        self.row_sum = []
        self.col_sum = []
        self.sum = 0

        for i in range(len(self.table)):
            temp = 0
            for j in range(len(self.table[0])):
                temp += self.table[i][j]
            self.row_sum.append(temp)
        
        for j in range(len(self.table[0])):
            temp = 0
            for i in range(len(self.table)):
                temp += self.table[i][j]
            self.col_sum.append(temp)
        
        for k in self.row_sum:
            self.sum += k
        
        self.p_part = 1
        for x in self.row_sum:
            self.p_part *= math.factorial(x)
        for y in self.col_sum:
            self.p_part *= math.factorial(y)
        self.p_part /= math.factorial(self.sum)

        self.p_0 = self.hyper_geom(self.table)
        self.p = 0
        #self.cnt = 0

        mat = [[0] * len(self.col_sum)] * len(self.row_sum)
        pos = (0, 0)

        self.dfs(mat, pos)

        #if self.cnt > 1000000:
        #    return np.NAN

        return self.p

    def dfs(self, mat, pos):

        #self.cnt += 1
        #if self.cnt > 1000000:
        #    return
        
        (xx, yy) = pos
        (rr, cc) = (len(self.row_sum), len(self.col_sum))

        mat_new = []

        for i in range(len(mat)):
            temp = []
            for j in range(len(mat[0])):
                temp.append(mat[i][j])
            mat_new.append(temp)

        if xx == -1 and yy == -1:
            for i in range(rr-1):
                temp = self.row_sum[i]
                for j in range(cc-1):
                    temp -= mat_new[i][j]
                mat_new[i][cc-1] = temp
            for j in range(cc-1):
                temp = self.col_sum[j]
                for i in range(rr-1):
                    temp -= mat_new[i][j]
                mat_new[rr-1][j] = temp
            temp = self.row_sum[rr-1]
            for j in range(cc-1):
                temp -= mat_new[rr-1][j]
            if temp <0:
                return
            mat_new[rr-1][cc-1] = temp
            
            p_1 = self.hyper_geom(mat_new)

            if p_1 <= self.p_0 + 0.000000000000000001:
                self.p += p_1
        else:
            max_1 = self.row_sum[xx]
            max_2 = self.col_sum[yy]
            for j in range(cc):
                max_1 -= mat_new[xx][j]
            for i in range(rr):
                max_2 -= mat_new[i][yy]
            for k in range(min(max_1,max_2)+1):
                mat_new[xx][yy] = k
                if xx == rr-2 and yy == cc-2:
                    pos_new = (-1, -1)
                elif xx == rr-2:
                    pos_new = (0, yy+1)
                else:
                    pos_new = (xx+1, yy)
                self.dfs(mat_new, pos_new)

    def hyper_geom(self, table):
        p = self.p_part
        for i in range(len(table)):
            for j in range(len(table[0])):
                p /= math.factorial(table[i][j])
        return p

def fisher_exact_test(data, variable_1, variable_2, kind="count"):
    '''
    Test whether there is an association between two categorical variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two categorical columns.
    variable_1 : :py:class:`str`
        The first categorical variable. Maximum 10 groups.
    variable_2 : :py:class:`str`
        The second categorical variable. Switching the two variables will not change the result of Fisher exact test. Maximum 10 groups.
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
        The p-value of the test.

    See also
    --------
    chi_square_test : The normal approximation version of Fisher exact test.
    binomial_test : Test the difference between the observed and expected proportion of a variable.

    Notes
    -----
    .. warning::
        Fisher exact test calculates the exact p-value by iterating through all the possible distributions, so it may consume lots of time when the size of data is huge. For larger data, :py:func:`chi_square_test` is recommended. 

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("fisher_exact_test.csv")
    >>> data
        Frequency     Result
    0     Monthly  Undamaged
    1     Monthly    Damaged
    2     Monthly    Damaged
    3     Monthly    Damaged
    4     Monthly  Undamaged
    ..        ...        ...
    95    Monthly  Undamaged
    96     Weekly  Undamaged
    97    Monthly    Damaged
    98  Quarterly  Undamaged
    99    Monthly  Undamaged

    We want to test whether there is an association between *Frequency* and *Result*.

    >>> summary, result = bs.fisher_exact_test(data=data, variable_1="Frequency", variable_2="Result", kind="horizontal")
    >>> summary
               Damaged  Undamaged
    Daily         0.04       0.96
    Monthly       0.56       0.44
    Quarterly     0.44       0.56
    Weekly        0.20       0.80

    The proportions of *Damaged* in different *Frequency* are given.

    >>> result
            p-value     
    Model  0.000123  ***

    The p-value < 0.001, so there is a significant association between *Frequency* and *Result*. That is, the proportions of *Damaged* are different between the four *Frequency*.

    '''

    data = data[list({variable_1, variable_2})].dropna()
    _process(data, cat=[variable_1, variable_2])

    if data[variable_1].nunique() > 10:
        raise Warning("The nmuber of classes in column '{}' cannot > 10.".format(variable_1))
    if data[variable_2].nunique() > 10:
        raise Warning("The nmuber of classes in column '{}' cannot > 10.".format(variable_2))

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

    test = fisher_exact(obs)
    p = _CC(lambda: test.calc())

    result = pd.DataFrame(
        {
            "p-value": _CC(lambda: p)
        }, index=["Model"]
    )
    
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result

def mcnemar_exact_test(data, variable_1, variable_2, pair):
    '''
    Test whether the proportions of a categorical variable are different in two paired groups.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two categorical columns, and a column specifying the pairs.
    variable_1 : :py:class:`str`
        The categorical variable that specifies which group the samples belong to. Maximum 10 groups. The most frequently appearing two groups will be chosen automatically.
    variable_2 : :py:class:`str`
        The categorical variable that we want to calculate proportions of. Maximum 10 groups. The most frequently appearing two groups will be chosen automatically.
    pair : :py:class:`str`
        The variable that specifies the pair ID. Samples in the same pair should have the same ID. Maximum 1000 pairs.

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The contingency table of the two categorical variables with matched pairs as the unit.
    result : :py:class:`pandas.DataFrame`
        The p-value of the test.

    See also
    --------
    mcnemar_test : The normal approximation version of McNemar's test,
    fisher_exact_test : Test the association between two categorical variables.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("mcnemar_exact_test.csv")
    >>> data
       Treatment Result  ID
    0    control   fail   1
    1    control   fail   2
    2    control   fail   3
    3    control   fail   4
    4    control   fail   5
    ..       ...    ...  ..
    83      test   pass  40
    84      test   pass  41
    85      test   pass  42
    86      test   pass  43
    87      test   pass  44

    We want to test whether the proportions of *Result* are different between the two *Treatment*, where each *control* is paired with a *test*.

    >>> summary, result = bs.mcnemar_exact_test(data=data, variable_1="Treatment", variable_2="Result", pair="ID")
    >>> summary
                    test : fail  test : pass
    control : fail           21            9
    control : pass            2           12

    The contingency table of *Treatment* and *Result* where the counting unit is the matched pair.

    >>> result
           p-value      
    Model  0.06543  <NA>

    The p-value > 0.05, so there is no significant difference between the proportions of *Result* under the two *Treatment*.

    '''

    data = data[list({variable_1, variable_2, pair})].dropna()
    _process(data, cat=[variable_1, variable_2, pair])
    
    if data[variable_1].nunique() > 10:
        raise Warning("The nmuber of classes in column '{}' cannot > 10.".format(variable_1))
    if data[variable_2].nunique() > 10:
        raise Warning("The nmuber of classes in column '{}' cannot > 10.".format(variable_2))
    if data[pair].nunique() > 1000:
        raise Warning("The nmuber of classes in column '{}' cannot > 1000.".format(pair))

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

    p = _CC(lambda: 0)
    n = _CC(lambda: b + c)
    if b < c:
        for x in range(0, b+1):
            p = _CC(lambda: p + math.factorial(n) / (math.factorial(x) * math.factorial(n-x) * 2**n))
        p = _CC(lambda: p * 2)
    elif b > c:
        for x in range(b, n+1):
            p = _CC(lambda: p + math.factorial(n) / (math.factorial(x) * math.factorial(n-x) * 2**n))
        p = _CC(lambda: p * 2)
    else: 
        p = _CC(lambda: 1)

    result = pd.DataFrame(
        {
            "p-value": _CC(lambda: p)
        }, index=["Model"]
    )
    _add_p(result)

    _process(summary)
    _process(result)

    return summary, result