import pandas as pd
import numpy as np
from scipy import stats as st
import math
from statsmodels.stats.proportion import proportion_confint
from factor_analyzer import FactorAnalyzer
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

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


def screening_test(data, disease, disease_target, test, test_target):

    process(data)
    data = data[list({disease, test})].dropna()

    if data[disease].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(disease))
    if data[test].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(test))

    TP = CC(data[(data[disease]==disease_target) & (data[test]==test_target)][disease].count)
    TN = CC(data[(data[disease]!=disease_target) & (data[test]!=test_target)][disease].count)
    FP = CC(data[(data[disease]!=disease_target) & (data[test]==test_target)][disease].count)
    FN = CC(data[(data[disease]==disease_target) & (data[test]!=test_target)][disease].count)

    summary = pd.DataFrame([[TP,FP],[FN,TN]])
    summary.index = ["{} (+)".format(test), "{} (-)".format(test)]
    summary.columns = ["{} (+)".format(disease), "{} (-)".format(disease)]

    """
    summary = pd.DataFrame(
        {
            "True Positive": TP ,
            "True Negative": TN ,
            "False Positive": FP ,
            "False Negative": FN
        }, index=["Case"]
    )    
    """

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

    process(summary)
    process(result)

    return summary, result


def epidemiologic_study(data, disease, disease_target, factor, factor_target):

    process(data)
    data = data[list({disease, factor})].dropna()

    if data[disease].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(disease))
    if data[factor].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(factor))

    data = data[[disease, factor]].dropna()

    a = CC(data[(data[disease]==disease_target) & (data[factor]==factor_target)][disease].count)
    b = CC(data[(data[disease]!=disease_target) & (data[factor]==factor_target)][disease].count)
    c = CC(data[(data[disease]==disease_target) & (data[factor]!=factor_target)][disease].count)
    d = CC(data[(data[disease]!=disease_target) & (data[factor]!=factor_target)][disease].count)


    summary = pd.DataFrame([[a,b],[c,d]])
    summary.index = ["{} (+)".format(factor), "{} (-)".format(factor)]
    summary.columns = ["{} (+)".format(disease), "{} (-)".format(disease)]

    n_1 = CC(lambda: a + b)
    n_2 = CC(lambda: c + d)
    p_1 = CC(lambda: a / n_1)
    p_2 = CC(lambda: c / n_2)
    p = CC(lambda: n_1 / (n_1 + n_2))

    RD = CC(lambda: p_1 - p_2)
    RD_l = CC(lambda: st.norm.ppf(0.025, RD, math.sqrt(p_1*(1-p_1)/n_1+p_2*(1-p_2)/n_2)))
    RD_h = CC(lambda: st.norm.ppf(0.975, RD, math.sqrt(p_1*(1-p_1)/n_1+p_2*(1-p_2)/n_2)))

    RR = CC(lambda: p_1 / p_2)
    RR_s = CC(lambda: math.sqrt(b/(a*n_1)+d/(c*n_2)))
    RR_l = CC(lambda: math.exp(st.norm.ppf(0.025, math.log(RR), RR_s)))
    RR_h = CC(lambda: math.exp(st.norm.ppf(0.975, math.log(RR), RR_s)))

    OR = CC(lambda: (a * d) / (b * c))
    OR_s = CC(lambda: math.sqrt(1/a+1/b+1/c+1/d))
    OR_l = CC(lambda: math.exp(st.norm.ppf(0.025, math.log(OR), OR_s)))
    OR_h = CC(lambda: math.exp(st.norm.ppf(0.975, math.log(OR), OR_s)))

    AR = CC(lambda: (RR-1) * p / ((RR-1) * p + 1))
    AR_s = CC(lambda: (RR / abs(RR-1)) * math.sqrt(b/(a*n_1)+d/(c*n_2)))
    AR_c1 = CC(lambda: st.norm.ppf(0.025, math.log(AR/(1-AR)), AR_s))
    AR_c2 = CC(lambda: st.norm.ppf(0.975, math.log(AR/(1-AR)), AR_s))
    AR_l = CC(lambda: math.exp(AR_c1) / (1 + math.exp(AR_c1)))
    AR_h = CC(lambda: math.exp(AR_c2) / (1 + math.exp(AR_c2)))

    table = []
    table.append([RD, RD_l, RD_h])
    table.append([RR, RR_l, RR_h])
    table.append([OR, OR_l, OR_h])
    table.append([AR, AR_l, AR_h])

    result = pd.DataFrame(table)
    result.index = ["Risk Difference", "Risk Ratio", "Odds Ratio", "Attributable Risk"]
    result.columns = ["Estimation", "95% CI: Lower", "95% CI: Upper"]

    process(summary)
    process(result)

    return summary, result


def factor_analysis(data, x, factors, analyze):

    process(data)
    data = data[list(set(x))].dropna()

    for var in x:
        if str(data[var].dtypes) != "float64":
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

    process(summary)
    process(result)
    process(analysis)

    return summary, result, analysis


def principal_component_analysis(data, x, transform=None):

    process(data)
    data = data[list(set(x))].dropna()

    for var in x:
        if str(data[var].dtypes) != "float64":
            raise Warning("The column '{}' must be numeric".format(var))

    summary = pd.DataFrame(
        {
            "Count" : [CC(data[var].count) for var in x] ,
            "Mean" : [CC(st.tmean, data[var].dropna()) for var in x] ,
            "Std. Deviation" : [CC(st.tstd, data[var].dropna()) for var in x] ,
            "Variance" : [CC(st.tvar, data[var].dropna()) for var in x]
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

    process(summary)
    process(result)
    process(transformation)

    return summary, result, transformation


def linear_discriminant_analysis(data, x, y, predict=None):

    process(data)
    data = data[list(set(x+[y]))].dropna()

    for var in x:
        if str(data[var].dtypes) != "float64":
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

    process(summary)
    process(result)
    process(prediction)

    return summary, result, prediction
    