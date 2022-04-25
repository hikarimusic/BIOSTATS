import numpy as np
import pandas as pd

from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

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
