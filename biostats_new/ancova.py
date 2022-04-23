import numpy as np
import pandas as pd

from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

'''
def one_way_anova(data=None, target=None, between=None, summary=None):
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

    if summary == 1:
        return result2
    else:
        return result
'''

def one_way_ancova(data=None, target=None, between=None, covariate=None, summary=None):

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

    if summary == 1:
        return result2
    else:
        return result

def two_way_ancova(data=None, target=None, between=None, covariate=None, summary=None):

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

    if summary == 1:
        return result2
    else:
        return result

def N_way_ancova(data=None, target=None, between=None, covariate=None, summary=None):

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

    if summary == 1:
        return result2
    else:
        return result

