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


def multiple_logistic_regression(data, x_nominal, x_categorical, y, target):
    
    process(data)
    data = data[list(set(x_nominal+x_categorical+[y]))].dropna()

    for var in x_nominal:
        if str(data[var].dtypes) != "float64":
            raise Warning("The column '{}' must be numeric".format(var))
    for var in x_categorical:
        if data[var].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(var))
    if data[y].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(y))

    data2 = data[x_nominal+x_categorical].copy()
    data2[y] = 0
    data2.loc[data[y]==target, y] = 1

    formula = "Q('%s') ~ " % y
    for var in x_nominal:
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
        for var in x_nominal:
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


def ordered_logistic_regression(data, x_nominal, x_categorical, y, order):
    
    process(data)
    data = data[list(set(x_nominal+x_categorical+[y]))].dropna()

    for var in x_nominal:
        if str(data[var].dtypes) != "float64":
            raise Warning("The column '{}' must be numeric".format(var))
    for var in x_categorical:
        if data[var].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(var))
    if data[y].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(y))

    data[y] = data[y].astype(pd.CategoricalDtype(categories=[x[0] for x in sorted(order.items(), key=lambda item: item[1])], ordered=True))

    formula = "%s ~ " % y
    for var in x_nominal:
        formula += "%s + " % var
    for var in x_categorical:
        formula += "C(%s) + " % var
    formula = formula[:-3]

    model = OrderedModel.from_formula(formula, data=data, distr="logit").fit(disp=False)

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


def multinomial_logistic_regression(data, x_nominal, x_categorical, y, baseline):
    
    process(data)
    data = data[list(set(x_nominal+x_categorical+[y]))].dropna()

    for var in x_nominal:
        if str(data[var].dtypes) != "float64":
            raise Warning("The column '{}' must be numeric".format(var))
    for var in x_categorical:
        if data[var].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(var))
    if data[y].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(y))

    group = data[y].dropna().unique().tolist()
    group.remove(baseline)

    data2 = data[x_nominal+x_categorical].copy()
    data2[y] = 0
    for i, cat in enumerate(group):
        data2.loc[data[y]==cat, y] = i+1

    formula = "%s ~ " % y
    for var in x_nominal:
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


