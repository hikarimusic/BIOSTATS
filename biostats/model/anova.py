import numpy as np
import pandas as pd
from scipy import stats as st

from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.multivariate.manova import MANOVA

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

def one_way_anova(data, variable, between):

    process(data)

    group = data[between].dropna().unique()

    summary = pd.DataFrame()

    for x in group:
        n = CC(data[data[between]==x][variable].dropna().count)
        mean = CC(data[data[between]==x][variable].dropna().mean)
        std = CC(data[data[between]==x][variable].dropna().std)
        sem = CC(data[data[between]==x][variable].dropna().sem)
        temp = pd.DataFrame(
            {
                "{}".format(between): x,
                "Count": n,
                "Mean": mean,
                "Std. Deviation": std,
                "95% CI: Lower" : CC(lambda: st.t.ppf(0.025, n-1, mean, sem)) ,
                "95% CI: Upper" : CC(lambda: st.t.ppf(0.975, n-1, mean, sem)) ,
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
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def two_way_anova(data, variable, between_1, between_2):

    process(data)

    group_1 = data[between_1].dropna().unique()
    group_2 = data[between_2].dropna().unique()

    summary = pd.DataFrame()

    for x in group_1:
        for y in group_2:
            n = CC(data[(data[between_1]==x) & (data[between_2]==y)][variable].dropna().count)
            mean = CC(data[(data[between_1]==x) & (data[between_2]==y)][variable].dropna().mean)
            std = CC(data[(data[between_1]==x) & (data[between_2]==y)][variable].dropna().std)
            sem = CC(data[(data[between_1]==x) & (data[between_2]==y)][variable].dropna().sem)
            temp = pd.DataFrame(
                {
                    "{}".format(between_1): x,
                    "{}".format(between_2): y,
                    "Count": n,
                    "Mean": mean,
                    "Std. Deviation": std,
                    "95% CI: Lower" : CC(lambda: st.t.ppf(0.025, n-1, mean, sem)) ,
                    "95% CI: Upper" : CC(lambda: st.t.ppf(0.975, n-1, mean, sem)) ,
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
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def one_way_ancova(data, variable, between, covariable):

    process(data)

    group = data[between].dropna().unique()

    summary = pd.DataFrame()

    for x in group:
        n = CC(data[data[between]==x][[variable, covariable]].dropna()[variable].count)
        mean_1 = CC(data[data[between]==x][[variable, covariable]].dropna()[variable].mean)
        std_1 = CC(data[data[between]==x][[variable, covariable]].dropna()[variable].std)
        mean_2 = CC(data[data[between]==x][[variable, covariable]].dropna()[covariable].mean)
        std_2 = CC(data[data[between]==x][[variable, covariable]].dropna()[covariable].std)
        temp = pd.DataFrame(
            {
                "{}".format(between): x,
                "Count": n,
                "Mean ({})".format(variable): mean_1,
                "Std. ({})".format(variable): std_1,
                "Mean ({})".format(covariable): mean_2,
                "Std. ({})".format(covariable): std_2,
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
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def two_way_ancova(data, variable, between_1, between_2, covariable):

    process(data)

    group_1 = data[between_1].dropna().unique()
    group_2 = data[between_2].dropna().unique()

    summary = pd.DataFrame()


    summary = pd.DataFrame()

    for x in group_1:
        for y in group_2:
            n = CC(data[(data[between_1]==x) & (data[between_2]==y)][[variable, covariable]].dropna()[variable].count)
            mean_1 = CC(data[(data[between_1]==x) & (data[between_2]==y)][[variable, covariable]].dropna()[variable].mean)
            std_1 = CC(data[(data[between_1]==x) & (data[between_2]==y)][[variable, covariable]].dropna()[variable].std)
            mean_2 = CC(data[(data[between_1]==x) & (data[between_2]==y)][[variable, covariable]].dropna()[covariable].mean)
            std_2 = CC(data[(data[between_1]==x) & (data[between_2]==y)][[variable, covariable]].dropna()[covariable].std)
            temp = pd.DataFrame(
                {
                    "{}".format(between_1): x,
                    "{}".format(between_2): y,
                    "Count": n,
                    "Mean ({})".format(variable): mean_1,
                    "Std. ({})".format(variable): std_1,
                    "Mean ({})".format(covariable): mean_2,
                    "Std. ({})".format(covariable): std_2,
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
    add_p(result)

    process(summary)
    process(result)

    return summary, result

def multivariate_anova(data, variable, between):

    process(data)

    group = data[between].dropna().unique().tolist()

    summary = pd.DataFrame({between:group})
    for var in variable:
        mean = []
        std = []
        for x in group:
            mean.append(CC(data[data[between]==x][var].dropna().mean))
            std.append(CC(data[data[between]==x][var].dropna().std))
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
            "D.F." : len(group)-1 ,
            "Pillai's Trace" : table.iloc[1][0] ,
            "F Statistic" : table.iloc[1][3] ,
            "p-value" : table.iloc[1][4]
        }, index=[between]
    )
    add_p(result)

    process(summary)
    process(result)

    return summary, result

def repeated_measures_anova(data, variable, between, subject):

    process(data)

    cross = pd.crosstab(index=data[subject], columns=data[between])
    for col in cross:
        cross = cross.drop(cross[cross[col] != 1].index)
    sub = cross.index.values.tolist()
    data = data[data[subject].isin(sub)]
    
    group = data[between].dropna().unique()

    summary = pd.DataFrame()

    for x in group:
        n = CC(data[data[between]==x][variable].dropna().count)
        mean = CC(data[data[between]==x][variable].dropna().mean)
        std = CC(data[data[between]==x][variable].dropna().std)
        sem = CC(data[data[between]==x][variable].dropna().sem)
        temp = pd.DataFrame(
            {
                "{}".format(between): x,
                "Count": n,
                "Mean": mean,
                "Std. Deviation": std,
                "95% CI: Lower" : CC(lambda: st.t.ppf(0.025, n-1, mean, sem)) ,
                "95% CI: Upper" : CC(lambda: st.t.ppf(0.975, n-1, mean, sem)) ,
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

    df_1 = anova_1.iloc[0][0]
    df_2 = df_1 * anova_2.iloc[0][0]
    SS_1 = anova_1.iloc[0][1]
    SS_2 = anova_2.iloc[1][1] - SS_1
    MS_1 = SS_1 / df_1
    MS_2 = SS_2 / df_2 
    F = MS_1 / MS_2
    p = 1 - st.f.cdf(F, df_1, df_2)

    result = pd.DataFrame(
        {
            "D.F." : [df_1, df_2] ,
            "Sum Square" : [SS_1, SS_2] ,
            "Mean Square" : [MS_1, MS_2] ,
            "F Statistic" : [F, None] ,
            "p-value" : [p, None]
        }, index = [between, "Residual"]
    )
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