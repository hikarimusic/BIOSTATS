import re
import numpy as np
import pandas as pd

from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from scipy import stats as st

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

    process(data)

    summary = pd.DataFrame(
        {
            "{}".format(between) : data.groupby(between, sort=False)[variable].groups.keys(),
            "Count": data.groupby(between, sort=False)[variable].count(),
            "Mean": data.groupby(between, sort=False)[variable].mean(),
            #"Std. Deviation": data.groupby(between, sort=False)[variable].std(),
            "Std. Deviation": CC(data.groupby(between, sort=False)[variable].std,),
            "Minimum": data.groupby(between, sort=False)[variable].min(),
            "1st Quartile": data.groupby(between, sort=False)[variable].quantile(0.25),
            "Median": data.groupby(between, sort=False)[variable].median(),
            "3rd Quartile": data.groupby(between, sort=False)[variable].quantile(0.75),
            "Maximum": data.groupby(between, sort=False)[variable].max(),
        }
    )

    summary.index.name = None
    summary = summary.reset_index(drop=True)
    summary.index += 1

    '''
    index_change = {}
    for index in result2.index:
        changed = "{}({})".format(between, index)
        index_change[index] = changed
    result2 = result2.rename(index_change)
    '''

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



















'''
def one_way_anova(data, target, between, summary=None):
    
    formula = "Q('%s') ~ " % target
    formula += "C(Q('%s'))" % between
    model = ols(formula, data=data).fit()
    result = anova_lm(model)
    result = result.rename(columns={
        'sum_sq' : 'Sum Square',
        'mean_sq' : 'Mean Square',
        'F' : 'F Statistic',
        'PR(>F)' : 'p-value'
    })
    result = result.rename(index={
        "C(Q('%s'))" % between : between
    })

    result2 = pd.DataFrame(
        {
            "Count": data.groupby(between)[target].count(),
            "Mean": data.groupby(between)[target].mean(),
            "Median": data.groupby(between)[target].median(),
            "Std.": data.groupby(between)[target].std(),
            "Variance": data.groupby(between)[target].var()
        }
    )
    result2.index.name = None
    index_change = {}
    for index in result2.index:
        changed = "{}({})".format(between, index)
        index_change[index] = changed
    result2 = result2.rename(index_change)

    if summary:
        return result2
    else:
        return result

def two_way_anova(data, target, between, summary=None):

    formula = "Q('%s') ~ " % target
    formula += "C(Q('%s'), Sum) * " % between[0]
    formula += "C(Q('%s'), Sum)" % between[1]
    model = ols(formula, data=data).fit()
    result = anova_lm(model)
    result = result.rename(columns={
        'sum_sq' : 'Sum Square',
        'mean_sq' : 'Mean Square',
        'F' : 'F Statistic',
        'PR(>F)' : 'p-value'
    })
    index_change = {}
    for index in result.index:
        changed = index
        for var in between:
            changed = changed.replace("C(Q('%s'), Sum)" % var, var)
        changed = changed.replace(":", " : ")
        index_change[index] = changed
    result = result.rename(index_change)

    result2 = pd.DataFrame(columns=["Count", "Mean", "Median", "Std.", "Variance"])
    for var in between:
        temp = pd.DataFrame(
            {
                "Count": data.groupby(var)[target].count(),
                "Mean": data.groupby(var)[target].mean(),
                "Median": data.groupby(var)[target].median(),
                "Std.": data.groupby(var)[target].std(),
                "Variance": data.groupby(var)[target].var()
            }
        )
        index_change = {}
        for index in temp.index:
            changed = "{}({})".format(var, index)
            index_change[index] = changed
        temp = temp.rename(index_change)
        result2 = pd.concat([result2, temp])

    if summary:
        return result2
    else:
        return result

def n_way_anova(data, target, between, summary=None):

    formula = "Q('%s') ~ " % target
    for var in between:
        formula += "C(Q('%s'), Sum) * " % var
    formula = formula[:-3]
    model = ols(formula, data=data).fit()

    result = anova_lm(model)
    result = result.rename(columns={
        'sum_sq' : 'Sum Square',
        'mean_sq' : 'Mean Square',
        'F' : 'F Statistic',
        'PR(>F)' : 'p-value'
    })
    index_change = {}
    for index in result.index:
        changed = index
        for var in between:
            changed = changed.replace("C(Q('%s'), Sum)" % var, var)
        changed = changed.replace(":", " : ")
        index_change[index] = changed
    result = result.rename(index_change)

    result2 = pd.DataFrame(columns=["Count", "Mean", "Median", "Std.", "Variance"])
    for var in between:
        temp = pd.DataFrame(
            {
                "Count": data.groupby(var)[target].count(),
                "Mean": data.groupby(var)[target].mean(),
                "Median": data.groupby(var)[target].median(),
                "Std.": data.groupby(var)[target].std(),
                "Variance": data.groupby(var)[target].var()
            }
        )
        index_change = {}
        for index in temp.index:
            changed = "{}({})".format(var, index)
            index_change[index] = changed
        temp = temp.rename(index_change)
        result2 = pd.concat([result2, temp])

    if summary:
        return result2
    else:
        return result

def one_way_ancova(data, target, between, covariate, summary=None):

    formula = "Q('%s') ~ " % target
    formula += "C(Q('%s'), Sum) + " % between
    formula += "Q('%s')" % covariate
    model = ols(formula, data=data).fit()

    result = anova_lm(model, typ=2)
    result = result.rename(columns={
        'sum_sq' : 'Sum Square',
        'F' : 'F Statistic',
        'PR(>F)' : 'p-value'
    })
    index_change = {}
    for index in result.index:
        changed = index
        changed = changed.replace("C(Q('%s'), Sum)" % between, between)
        changed = changed.replace("Q('%s')" % covariate, covariate)
        index_change[index] = changed
    result = result.rename(index_change)

    result2 = pd.DataFrame(
        {
            "Count": data.groupby(between)[target].count(),
            "Mean": data.groupby(between)[target].mean(),
            "Std.": data.groupby(between)[target].std(),
        }
    )
    result2["Mean({})".format(covariate)] = data.groupby(between)[covariate].mean()
    result2.index.name = None
    index_change = {}
    for index in result2.index:
        changed = "{}({})".format(between, index)
        index_change[index] = changed
    result2 = result2.rename(index_change)

    if summary:
        return result2
    else:
        return result

def two_way_ancova(data, target, between, covariate, summary=None):

    formula = "Q('%s') ~ " % target
    formula += "C(Q('%s'), Sum) + " % between
    for var in covariate:
        formula += "Q('%s') + " % var
    formula = formula[:-3]
    model = ols(formula, data=data).fit()

    result = anova_lm(model, typ=2)
    result = result.rename(columns={
        'sum_sq' : 'Sum Square',
        'F' : 'F Statistic',
        'PR(>F)' : 'p-value'
    })
    index_change = {}
    for index in result.index:
        changed = index
        changed = changed.replace("C(Q('%s'), Sum)" % between, between)
        for var in covariate:
            changed = changed.replace("Q('%s')" % var, var)
        index_change[index] = changed
    result = result.rename(index_change)

    result2 = pd.DataFrame(
        {
            "Count": data.groupby(between)[target].count(),
            "Mean": data.groupby(between)[target].mean(),
            "Std.": data.groupby(between)[target].std(),
        }
    )
    for var in covariate:
        result2["Mean({})".format(var)] = data.groupby(between)[var].mean()
    result2.index.name = None
    index_change = {}
    for index in result2.index:
        changed = "{}({})".format(between, index)
        index_change[index] = changed
    result2 = result2.rename(index_change)

    if summary:
        return result2
    else:
        return result

def n_way_ancova(data, target, between, covariate, summary=None):

    formula = "Q('%s') ~ " % target
    formula += "C(Q('%s'), Sum) + " % between
    for var in covariate:
        formula += "Q('%s') + " % var
    formula = formula[:-3]
    model = ols(formula, data=data).fit()

    result = anova_lm(model, typ=2)
    result = result.rename(columns={
        'sum_sq' : 'Sum Square',
        'F' : 'F Statistic',
        'PR(>F)' : 'p-value'
    })
    index_change = {}
    for index in result.index:
        changed = index
        changed = changed.replace("C(Q('%s'), Sum)" % between, between)
        for var in covariate:
            changed = changed.replace("Q('%s')" % var, var)
        index_change[index] = changed
    result = result.rename(index_change)

    result2 = pd.DataFrame(
        {
            "Count": data.groupby(between)[target].count(),
            "Mean": data.groupby(between)[target].mean(),
            "Std.": data.groupby(between)[target].std(),
        }
    )
    for var in covariate:
        result2["Mean({})".format(var)] = data.groupby(between)[var].mean()
    result2.index.name = None
    index_change = {}
    for index in result2.index:
        changed = "{}({})".format(between, index)
        index_change[index] = changed
    result2 = result2.rename(index_change)

    if summary:
        return result2
    else:
        return result
'''