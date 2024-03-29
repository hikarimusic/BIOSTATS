import pandas as pd
import numpy as np
from scipy import stats as st
import math
from statsmodels.stats.proportion import proportion_confint
from factor_analyzer import FactorAnalyzer
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from biostats.model.util import _CC, _process, _add_p

def screening_test(data, disease, disease_target, test, test_target):
    '''
    Compute some common statistics of a screening test.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two categorical columns. 
    disease : :py:class:`str`
        The variable specifying the disease (or condition). Maximum 20 groups.
    disease_target : :py:class:`str`
        The group of the disease variable that is considered "positive".
    test : :py:class:`str`
        The variable specifying the test (or symptom). Maximum 20 groups.
    test_target : :py:class:`str`
        The group of the test variable that is considered "positive".

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The contingency table of true positive, true negative, false positive, and false negative.
    result : :py:class:`pandas.DataFrame`
        The values and confidence intervals of sensitivity (recall), specificity (selectivity), positive predictive value (precision), negative predictive value, accuracy, and prevalence. 

    See also
    --------
    epidemiologic_study : Compute some common statistics of an epidemiologic study.
    contingency : Compute the contingency table of two categorical variables.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("screening_test.csv")
    >>> data
          Cancer  PSA Test
    0    Present  Negative
    1     Absent  Negative
    2    Present  Positive
    3     Absent  Negative
    4    Present  Positive
    ..       ...       ...
    232  Present  Negative
    233  Present  Positive
    234  Present  Negative
    235   Absent  Negative
    236  Present  Positive

    We want to compute the sensitivity, specificity and so on of the screening test that detect *Cancer* from *PSA Test*.

    >>> summary, result = bs.screening_test(data=data, disease="Cancer", disease_target="Present", test="PSA Test", test_target="Positive")
    >>> summary
                  Cancer (+)  Cancer (-)
    PSA Test (+)          92          27
    PSA Test (-)          46          72

    The contingency table of TP (true positive), TN, FP and FN is given.

    >>> result
                 Estimation  95% CI: Lower  95% CI: Upper
    Sensitivity    0.666667       0.584443       0.739862
    Specificity    0.727273       0.632291       0.805276
    Positive PV    0.773109       0.690014       0.839123
    Negative PV    0.610169       0.520027       0.693365
    Accuracy       0.691983       0.630534       0.747308
    Prevalence     0.582278       0.518666       0.643266

    The values and confidence intervals of sensitivity, specificity and so on are computed.

    '''

    data = data[list({disease, test})].dropna()
    _process(data, cat=[disease, test])

    if data[disease].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(disease))
    if data[test].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(test))

    TP = _CC(data[(data[disease]==disease_target) & (data[test]==test_target)][disease].count)
    TN = _CC(data[(data[disease]!=disease_target) & (data[test]!=test_target)][disease].count)
    FP = _CC(data[(data[disease]!=disease_target) & (data[test]==test_target)][disease].count)
    FN = _CC(data[(data[disease]==disease_target) & (data[test]!=test_target)][disease].count)

    summary = pd.DataFrame([[TP,FP],[FN,TN]])
    summary.index = ["{} (+)".format(test), "{} (-)".format(test)]
    summary.columns = ["{} (+)".format(disease), "{} (-)".format(disease)]

    table = []
    table.append([TP/(TP+FN)] + list(proportion_confint(TP, TP+FN, method="wilson")))
    table.append([TN/(TN+FP)] + list(proportion_confint(TN, TN+FP, method="wilson")))
    table.append([TP/(TP+FP)] + list(proportion_confint(TP, TP+FP, method="wilson")))
    table.append([TN/(TN+FN)] + list(proportion_confint(TN, TN+FN, method="wilson")))
    table.append([(TP+TN)/(TP+TN+FP+FN)] + list(proportion_confint(TP+TN, TP+TN+FP+FN, method="wilson")))
    table.append([(TP+FN)/(TP+TN+FP+FN)] + list(proportion_confint(TP+FN, TP+TN+FP+FN, method="wilson")))

    result = pd.DataFrame(table)
    result.index = ["Sensitivity", "Specificity", "Positive PV", "Negative PV", "Accuracy", "Prevalence"]
    result.columns = ["Estimation", "95% CI: Lower", "95% CI: Upper"]

    _process(summary)
    _process(result)

    return summary, result


def epidemiologic_study(data, disease, disease_target, factor, factor_target):
    '''
    Compute some common statistics of an epidemiologic study.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two categorical columns. 
    disease : :py:class:`str`
        The variable specifying the disease. Maximum 20 groups.
    disease_target : :py:class:`str`
        The group of the disease variable that is considered "positive".
    factor : :py:class:`str`
        The variable specifying the factor. Maximum 20 groups.
    factor_target : :py:class:`str`
        The group of the factor variable that is considered "positive".

    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The contingency table of the disease and factor.
    result : :py:class:`pandas.DataFrame`
        The values and confidence intervals of risk difference, risk ratio (relative risk), odds ratio, and attributable risk.

    See also
    --------
    screening_test : Compute some common statistics of a screening test.
    contingency : Compute the contingency table of two categorical variables.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("epidemiologic_study.csv")
    >>> data
                 MI Diabetes
    0     Not occur       No
    1     Not occur       No
    2     Not occur       No
    3     Not occur       No
    4     Not occur       No
    ...         ...      ...
    2993  Not occur       No
    2994  Not occur       No
    2995  Not occur       No
    2996  Not occur       No
    2997  Not occur       No

    We want to compute the risk ratio, odds ratio and so on of the epidemiologic study that investigates the relation between *MI* and *Diabetes*.

    >>> summary, result = bs.epidemiologic_study(data=data, disease="MI", disease_target="Occur", factor="Diabetes", factor_target="Yes")
    >>> summary
                  MI (+)  MI (-)
    Diabetes (+)      48     183
    Diabetes (-)     210    2557

    The contingency table of *MI* and *Diabetes* is given.

    >>> result
                       Estimation  95% CI: Lower  95% CI: Upper
    Risk Difference      0.131898       0.078654       0.185141
    Risk Ratio           2.737910       2.062282       3.634880
    Odds Ratio           3.193755       2.256038       4.521233
    Attributable Risk    0.118094       0.078925       0.173051

    The values and confidence intervals of risk ratio, odds ratio and so on are computed.

    '''

    data = data[list({disease, factor})].dropna()
    _process(data, cat=[disease, factor])

    if data[disease].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(disease))
    if data[factor].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(factor))

    data = data[[disease, factor]].dropna()

    a = _CC(data[(data[disease]==disease_target) & (data[factor]==factor_target)][disease].count)
    b = _CC(data[(data[disease]!=disease_target) & (data[factor]==factor_target)][disease].count)
    c = _CC(data[(data[disease]==disease_target) & (data[factor]!=factor_target)][disease].count)
    d = _CC(data[(data[disease]!=disease_target) & (data[factor]!=factor_target)][disease].count)


    summary = pd.DataFrame([[a,b],[c,d]])
    summary.index = ["{} (+)".format(factor), "{} (-)".format(factor)]
    summary.columns = ["{} (+)".format(disease), "{} (-)".format(disease)]

    n_1 = _CC(lambda: a + b)
    n_2 = _CC(lambda: c + d)
    p_1 = _CC(lambda: a / n_1)
    p_2 = _CC(lambda: c / n_2)
    p = _CC(lambda: n_1 / (n_1 + n_2))

    RD = _CC(lambda: p_1 - p_2)
    RD_l = _CC(lambda: st.norm.ppf(0.025, RD, math.sqrt(p_1*(1-p_1)/n_1+p_2*(1-p_2)/n_2)))
    RD_h = _CC(lambda: st.norm.ppf(0.975, RD, math.sqrt(p_1*(1-p_1)/n_1+p_2*(1-p_2)/n_2)))

    RR = _CC(lambda: p_1 / p_2)
    RR_s = _CC(lambda: math.sqrt(b/(a*n_1)+d/(c*n_2)))
    RR_l = _CC(lambda: math.exp(st.norm.ppf(0.025, math.log(RR), RR_s)))
    RR_h = _CC(lambda: math.exp(st.norm.ppf(0.975, math.log(RR), RR_s)))

    OR = _CC(lambda: (a * d) / (b * c))
    OR_s = _CC(lambda: math.sqrt(1/a+1/b+1/c+1/d))
    OR_l = _CC(lambda: math.exp(st.norm.ppf(0.025, math.log(OR), OR_s)))
    OR_h = _CC(lambda: math.exp(st.norm.ppf(0.975, math.log(OR), OR_s)))

    AR = _CC(lambda: (RR-1) * p / ((RR-1) * p + 1))
    AR_s = _CC(lambda: (RR / abs(RR-1)) * math.sqrt(b/(a*n_1)+d/(c*n_2)))
    AR_c1 = _CC(lambda: st.norm.ppf(0.025, math.log(AR/(1-AR)), AR_s))
    AR_c2 = _CC(lambda: st.norm.ppf(0.975, math.log(AR/(1-AR)), AR_s))
    AR_l = _CC(lambda: math.exp(AR_c1) / (1 + math.exp(AR_c1)))
    AR_h = _CC(lambda: math.exp(AR_c2) / (1 + math.exp(AR_c2)))

    table = []
    table.append([RD, RD_l, RD_h])
    table.append([RR, RR_l, RR_h])
    table.append([OR, OR_l, OR_h])
    table.append([AR, AR_l, AR_h])

    result = pd.DataFrame(table)
    result.index = ["Risk Difference", "Risk Ratio", "Odds Ratio", "Attributable Risk"]
    result.columns = ["Estimation", "95% CI: Lower", "95% CI: Upper"]

    _process(summary)
    _process(result)

    return summary, result


def factor_analysis(data, x, factors, analyze=None):
    '''
    Find the underlying factors of a set of variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two numeric columns.
    x : :py:class:`list`
        The list of numeric variables to be analyzed.
    factors : :py:class:`int`
        The number of factors.
    analyze : :py:class:`dict`
        The data to be analyzed. Optional.
    
    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The uniqueness of each variable.
    result : :py:class:`pandas.DataFrame`
        The loadings of each variable, sum of squared loadings, proportion of variance, and cumulative proportion of variance of each factor.
    analysis : :py:class:`pandas.DataFrame`
        The factor scores of the data to be analyzed.
    
    See also
    --------
    principal_component_analysis : Find the linear combination of a set of variables to manifest the variation of data.
    linear_discriminant_analysis : Find the linear combination of a set of variables to distinguish between groups.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("factor_analysis.csv")
    >>> data
         Oil  Density  Crispy  Fracture  Hardness
    0   16.5     2955      10        23        97
    1   17.7     2660      14         9       139
    2   16.2     2870      12        17       143
    3   16.7     2920      10        31        95
    4   16.3     2975      11        26       143
    5   19.1     2790      13        16       189
    6   18.4     2750      13        17       114
    7   17.5     2770      10        26        63
    8   15.7     2955      11        23       123
    9   16.4     2945      11        24       132
    10  18.0     2830      12        15       121
    11  17.4     2835      12        18       172
    12  18.4     2860      14        11       170
    13  13.9     2965      12        19       169
    14  15.8     2930       9        26        65
    15  16.4     2770      15        16       183
    16  18.9     2650      14        20       114
    17  17.3     2890      12        17       142
    18  16.7     2695      13        13       111
    19  19.1     2755      14        10       140
    20  13.7     3000      10        27       177
    21  14.7     2980      10        20       133
    22  18.1     2780      13        14       150
    23  17.2     2705       8        27       113
    24  18.7     2825      13        20       166
    25  18.1     2875      12        15       150
    26  16.6     2945      10        25       100
    27  17.1     2920      10        25       123
    28  17.4     2845      13        19       129
    29  19.4     2645      12        18        68
    30  15.9     3080      10        23       106
    31  17.1     2825      10        28       131
    32  15.5     3125       7        33        92
    33  17.7     2780      13        22       141
    34  15.9     2900      12        21       192
    35  21.2     2570      14        13       105
    36  19.5     2635      13        22       101
    37  20.5     2725      14        16       145
    38  17.0     2865      11        22       100
    39  16.7     2975      10        26       105
    40  16.8     2980      10        24       144
    41  16.8     2870      12        20       123
    42  16.3     2920      11        22       136
    43  16.2     3100       8        27       140
    44  18.1     2910      12        21       120
    45  16.6     2865      11        25       120
    46  16.4     2995      12        20       165
    47  15.1     2925      10        29       118
    48  21.1     2700      13        16       116
    49  16.3     2845      10        26        75

    We want to find the underlying factors of the five variables.

    >>> summary, result, analysis = bs.factor_analysis(data=data, x=["Oil", "Density", "Crispy", "Fracture", "Hardness"], factors=2, 
    ...     analyze={"Oil":17.2, "Density":2830, "Crispy":12, "Fracture":19, "Hardness":121})
    >>> summary
                     Oil   Density   Crispy  Fracture  Hardness
    Uniqueness  0.322983  0.169086  0.04781  0.251765  0.398991

    The uniqueness of each variable (proportion of variability that cannot be explained by the factors) are given.

    >>> result
                     Factor 1  Factor 2
    Oil             -0.822497 -0.022736
    Density          0.911124  0.027689
    Crispy          -0.747793  0.626893
    Fracture         0.653877 -0.566286
    Hardness         0.095274  0.769371
                        NaN       NaN
    SS Loadings      2.502476  1.306891
    Proportion Var.  0.500495  0.261378
    Cumulative Var.  0.500495  0.761873

    The loadings (contribution of each original variable to the factor), SS Loadings (sum of squared loadings), Proportion Var (proportion of variance explained by each factor), and Cumulative Var (cumulative proportion of variance) are calculated.

    >>> analysis
              Factor 1  Factor 2
    Analysis -0.251185  0.090308

    The factor scores of the data to be analyzed are calculated.
    
    '''

    data = data[list(set(x))].dropna()
    _process(data, num=x)

    for var in x:
        if str(data[var].dtypes) not in ("float64", "Int64"):
            raise Warning("The column '{}' must be numeric".format(var))

    fa = FactorAnalyzer(n_factors=factors, rotation='varimax')
    fa.fit(data[x])

    summary = pd.DataFrame(np.expand_dims(fa.get_uniquenesses(), axis=0))
    summary.index = ["Uniqueness"]
    summary.columns = x

    loadings = pd.DataFrame(fa.loadings_)
    loadings.index = x
    loadings.columns = ["Factor {}".format(i+1) for i in range(factors)]

    blank = pd.DataFrame([[np.nan]*factors])
    blank.index = [""]
    blank.columns = ["Factor {}".format(i+1) for i in range(factors)]

    var = pd.DataFrame(np.array(fa.get_factor_variance()))
    var.index = ["SS Loadings", "Proportion Var.", "Cumulative Var."]
    var.columns = ["Factor {}".format(i+1) for i in range(factors)]

    result = pd.concat([loadings, blank, var])

    if analyze:
        analysis = pd.DataFrame(fa.transform(pd.DataFrame(analyze, index=[0])))
        analysis.columns = ["Factor {}".format(i+1) for i in range(factors)]
        analysis.index = ["Analysis"]
    else:
        analysis = pd.DataFrame()

    _process(summary)
    _process(result)
    _process(analysis)

    return summary, result, analysis


def principal_component_analysis(data, x, transform=None):
    '''
    Find the linear combination of a set of variables to manifest the variation of data.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column.
    x : :py:class:`list`
        The list of numeric variables to be analyzed.
    transform : :py:class:`dict`
        The data to be transformed. Optional.
    
    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The counts, mean values, standard deviations, and variances of each variable.
    result : :py:class:`pandas.DataFrame`
        The coefficients and intercepts of the linear combinations, as well as the proportions of variation explained by each dimension.
    transformation : :py:class:`pandas.DataFrame`
        The new coordinates of the data to be transformed.
    
    See also
    --------
    factor_analysis : Find the underlying factors of a set of variables.
    linear_discriminant_analysis : Find the linear combination of a set of variables to distinguish between groups.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("principal_component_analysis.csv")
    >>> data
        Murder  Assault  UrbanPop  Rape
    0     13.2      236        58  21.2
    1     10.0      263        48  44.5
    2      8.1      294        80  31.0
    3      8.8      190        50  19.5
    4      9.0      276        91  40.6
    5      7.9      204        78  38.7
    6      3.3      110        77  11.1
    7      5.9      238        72  15.8
    8     15.4      335        80  31.9
    9     17.4      211        60  25.8
    10     5.3       46        83  20.2
    11     2.6      120        54  14.2
    12    10.4      249        83  24.0
    13     7.2      113        65  21.0
    14     2.2       56        57  11.3
    15     6.0      115        66  18.0
    16     9.7      109        52  16.3
    17    15.4      249        66  22.2
    18     2.1       83        51   7.8
    19    11.3      300        67  27.8
    20     4.4      149        85  16.3
    21    12.1      255        74  35.1
    22     2.7       72        66  14.9
    23    16.1      259        44  17.1
    24     9.0      178        70  28.2
    25     6.0      109        53  16.4
    26     4.3      102        62  16.5
    27    12.2      252        81  46.0
    28     2.1       57        56   9.5
    29     7.4      159        89  18.8
    30    11.4      285        70  32.1
    31    11.1      254        86  26.1
    32    13.0      337        45  16.1
    33     0.8       45        44   7.3
    34     7.3      120        75  21.4
    35     6.6      151        68  20.0
    36     4.9      159        67  29.3
    37     6.3      106        72  14.9
    38     3.4      174        87   8.3
    39    14.4      279        48  22.5
    40     3.8       86        45  12.8
    41    13.2      188        59  26.9
    42    12.7      201        80  25.5
    43     3.2      120        80  22.9
    44     2.2       48        32  11.2
    45     8.5      156        63  20.7
    46     4.0      145        73  26.2
    47     5.7       81        39   9.3
    48     2.6       53        66  10.8
    49     6.8      161        60  15.6

    We want to find the linear combination of the four variables to manifest the variation of data.

    >>> summary, result, transformation = bs.principal_component_analysis(data=data, x=["Murder", "Assault", "UrbanPop", "Rape"], 
    ...     transform={"Murder":10.2, "Assault":211, "UrbanPop":67, "Rape":32.3})
    >>> summary
              Count     Mean  Std. Deviation     Variance
    Murder       50    7.788        4.355510    18.970465
    Assault      50  170.760       83.337661  6945.165714
    UrbanPop     50   65.540       14.474763   209.518776
    Rape         50   21.232        9.366385    87.729159

    Basic descriptive statistics of the four variables are calculated.

    >>> result
                   Murder   Assault  UrbanPop      Rape   Intercept  Proportion
    Dimension 1  0.041704  0.995221  0.046336  0.075156 -174.901326    0.965534
    Dimension 2  0.044822  0.058760 -0.976857 -0.200718   57.901952    0.027817
    Dimension 3  0.079891 -0.067570 -0.200546  0.974081    3.378144    0.005800
    Dimension 4  0.994922 -0.038938  0.058169 -0.072325   -3.376148    0.000849

    The coefficients and intercepts to form the new dimensions are given. The proportions of variation explained by each dimension are also given.

    >>> transformation
                    Dimension 1  Dimension 2  Dimension 3  Dimension 4
    Transformation    41.047766    -1.175146     7.962017     0.117308

    The new coordinates of the data to be transformed.
    
    '''

    data = data[list(set(x))].dropna()
    _process(data, num=x)

    for var in x:
        if str(data[var].dtypes) not in ("float64", "Int64"):
            raise Warning("The column '{}' must be numeric".format(var))

    summary = pd.DataFrame(
        {
            "Count" : [_CC(data[var].count) for var in x] ,
            "Mean" : [_CC(st.tmean, data[var].dropna()) for var in x] ,
            "Std. Deviation" : [_CC(st.tstd, data[var].dropna()) for var in x] ,
            "Variance" : [_CC(st.tvar, data[var].dropna()) for var in x]
        }, index=x
    )

    #for var in x:
    #    data[var] = (data[var] - data[var].mean()) / data[var].std()

    clf = PCA()
    clf.fit(data[x])

    weight = clf.transform(pd.DataFrame(np.identity(len(x)), columns=x))-clf.transform(pd.DataFrame(np.zeros((len(x), len(x))), columns=x))
    intercept = clf.transform(pd.DataFrame(np.zeros((1,len(x))), columns=x))
    proportion = np.expand_dims(clf.explained_variance_ratio_, axis=0)
    weight = np.concatenate((weight, intercept, proportion), axis=0)

    result = pd.DataFrame(weight.T)
    result.columns = x + ["Intercept", "Proportion"]
    result.index = ["Dimension {}".format(i+1) for i in range(len(result))]

    if transform:
        transformation = pd.DataFrame(clf.transform(pd.DataFrame(transform, index=[0])))
        transformation.columns = ["Dimension {}".format(i+1) for i in range(len(result))]
        transformation.index = ["Transformation"]
    else:
        transformation = pd.DataFrame()

    _process(summary)
    _process(result)
    _process(transformation)

    return summary, result, transformation


def linear_discriminant_analysis(data, x, y, predict=None):
    '''
    Find the linear combination of a set of variables to distinguish between groups.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column.
    x : :py:class:`list`
        The list of numeric variables to be analyzed.
    y : :py:class:`str`
        The categorical variable that specifies the groups to be distinguished. Maximum 20 groups.
    predict : :py:class:`dict`
        The data to be predicted. Optional.
    
    Returns
    -------
    summary : :py:class:`pandas.DataFrame`
        The mean values of each variable in each group.
    result : :py:class:`pandas.DataFrame`
        The coefficients and intercepts of the linear combinations, as well as the proportions of separation achieved by each dimension.
    prediction : :py:class:`pandas.DataFrame`
        The probabilities and results of the data to be predicted.
    
    See also
    --------
    factor_analysis : Find the underlying factors of a set of variables.
    principal_component_analysis : Find the linear combination of a set of variables to manifest the variation of data.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("linear_discriminant_analysis.csv")
    >>> data
        sepal_length sepal_width petal_length petal_width    species
    0            5.1         3.5          1.4         0.2     setosa
    1            4.9         3.0          1.4         0.2     setosa
    2            4.7         3.2          1.3         0.2     setosa
    3            4.6         3.1          1.5         0.2     setosa
    4            5.0         3.6          1.4         0.2     setosa
    ..           ...         ...          ...         ...        ...
    145          6.7         3.0          5.2         2.3  virginica
    146          6.3         2.5          5.0         1.9  virginica
    147          6.5         3.0          5.2         2.0  virginica
    148          6.2         3.4          5.4         2.3  virginica
    149          5.9         3.0          5.1         1.8  virginica

    We want to find the linear combination of the four variables to distinguish between the three *species*.

    >>> summary, result, prediction = bs.linear_discriminant_analysis(data=data, x=["sepal_length", "sepal_width", "petal_length" ,"petal_width"], y="species", 
    ...     predict={"sepal_length": 5.7, "sepal_width": 2.7, "petal_length": 4.0 ,"petal_width":1.4})
    >>> summary
                sepal_length  sepal_width  petal_length  petal_width
    setosa             5.006        3.428         1.462        0.246
    versicolor         5.936        2.770         4.260        1.326
    virginica          6.588        2.974         5.552        2.026

    The mean values of each variable in each group are calculated.

    >>> result
                 sepal_length  sepal_width  petal_length  petal_width  Intercept  Proportion
    Dimension 1      0.829378     1.534473     -2.201212    -2.810460   2.105106    0.991213
    Dimension 2      0.024102     2.164521     -0.931921     2.839188  -6.661473    0.008787

    The coefficients and intercepts to form the new dimensions are given. The proportions of separation achieved by each dimension are also given.

    >>> prediction
                   P(setosa)  P(versicolor)  P(virginica)      Result
    Prediction  7.206674e-20       0.999792      0.000208  versicolor

    The data is predicted to belong to *versicolor*.
    
    '''

    data = data[list(set(x+[y]))].dropna()
    _process(data, num=x, cat=[y])
    
    for var in x:
        if str(data[var].dtypes) not in ("float64", "Int64"):
            raise Warning("The column '{}' must be numeric".format(var))
    if data[y].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(y))

    clf = LinearDiscriminantAnalysis()
    clf.fit(data[x], data[y])

    mean_ = clf.means_
    summary = pd.DataFrame(mean_)
    summary.columns = x
    summary.index = clf.classes_

    weight = clf.transform(pd.DataFrame(np.identity(len(x)), columns=x))-clf.transform(pd.DataFrame(np.zeros((len(x), len(x))), columns=x))
    intercept = clf.transform(pd.DataFrame(np.zeros((1,len(x))), columns=x))
    proportion = np.expand_dims(clf.explained_variance_ratio_, axis=0)
    weight = np.concatenate((weight, intercept, proportion), axis=0)

    result = pd.DataFrame(weight.T)
    result.columns = x + ["Intercept", "Proportion"]
    result.index = ["Dimension {}".format(i+1) for i in range(len(result))]

    if predict:
        prob = clf.predict_proba(pd.DataFrame(predict, index=[0]))
        kind = np.expand_dims(clf.predict(pd.DataFrame(predict, index=[0])), axis=0)
        prediction = pd.DataFrame(np.concatenate((prob, kind), axis=1))
        prediction.columns = ["P({})".format(x) for x in clf.classes_] + ["Result"]
        prediction.index = ["Prediction"]
    else:
        prediction = pd.DataFrame()

    _process(summary)
    _process(result)
    _process(prediction)

    return summary, result, prediction
    