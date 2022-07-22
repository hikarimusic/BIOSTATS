import pandas as pd
import numpy as np
from scipy import stats as st
import math

from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

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


def one_sample_t_test(data, variable, expect, kind="two-side"):

    process(data)
    data = data[[variable]].dropna()

    if str(data[variable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(variable))

    n = CC(lambda a: a.count(), data[variable].dropna())
    mean = CC(st.tmean, data[variable].dropna())
    sem = CC(st.tsem, data[variable].dropna())

    if kind == "two-side":
        summary = pd.DataFrame(
            {
                "Estimate" : CC(lambda: mean) ,
                "Std. Error" : CC(lambda: sem) ,
                "95% CI: Lower" : CC(lambda: st.t.ppf(0.025, n-1, mean, sem)) ,
                "95% CI: Upper" : CC(lambda: st.t.ppf(0.975, n-1, mean, sem)) ,
            }, index=[variable]
        )
        t = CC(lambda: (mean-expect)/sem)
        p = CC(lambda: st.t.cdf(t, n-1))
        p = CC(lambda: 2*min(p, 1-p))
        result = pd.DataFrame(
            {
                "D.F." : CC(lambda: n-1) ,
                "t Statistic" : CC(lambda: t) ,
                "p-value" : CC(lambda: p)
            }, index=["Model"]
        )
    elif kind == "greater":
        summary = pd.DataFrame(
            {
                "Estimate" : CC(lambda: mean) ,
                "Std. Error" : CC(lambda: sem) ,
                "95% CI: Lower" : CC(lambda: st.t.ppf(0.05, n-1, mean, sem)) ,
                "95% CI: Upper" : "Inf" ,
            }, index=[variable]
        )
        t = CC(lambda: (mean-expect)/sem)
        p = CC(lambda: st.t.cdf(t, n-1))
        p = CC(lambda: 1-p)
        result = pd.DataFrame(
            {
                "D.F." : CC(lambda: n-1) ,
                "t Statistic" : CC(lambda: t) ,
                "p-value" : CC(lambda: p)
            }, index=["Model"]
        )
    elif kind == "less":
        summary = pd.DataFrame(
            {
                "Estimate" : CC(lambda: mean) ,
                "Std. Error" : CC(lambda: sem) ,
                "95% CI: Lower" : "-Inf" ,
                "95% CI: Upper" : CC(lambda: st.t.ppf(0.95, n-1, mean, sem)) ,
            }, index=[variable]
        )
        t = CC(lambda: (mean-expect)/sem)
        p = CC(lambda: st.t.cdf(t, n-1))
        result = pd.DataFrame(
            {
                "D.F." : CC(lambda: n-1) ,
                "t Statistic" : CC(lambda: t) ,
                "p-value" : CC(lambda: p)
            }, index=["Model"]
        )
    else:
        return

    add_p(result)

    process(summary)
    process(result)

    return summary, result


def two_sample_t_test(data, variable, between, group, kind="equal variances"):

    process(data)
    data = data[list({variable, between})].dropna()

    if str(data[variable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))

    n, mean, std, sem = [None] * 2, [None] * 2, [None] * 2, [None] * 2
    for i, cat, in enumerate(group):
        n[i]    = CC(data[data[between]==cat][variable].dropna().count)
        mean[i] = CC(st.tmean, data[data[between]==cat][variable].dropna())
        std[i]  = CC(st.tstd, data[data[between]==cat][variable].dropna())
        sem[i]  = CC(st.tsem, data[data[between]==cat][variable].dropna())

    summary = pd.DataFrame(
        {
            "Estimate" : CC(lambda: mean) ,
            "Std. Error" : CC(lambda: sem) ,
            "95% CI: Lower" : [CC(lambda: st.t.ppf(0.025, n[i]-1, mean[i], sem[i])) for i in range(2)] ,
            "95% CI: Upper" : [CC(lambda: st.t.ppf(0.975, n[i]-1, mean[i], sem[i])) for i in range(2)] ,
        }, index=group
    )

    if kind == "equal variances":
        _mean = CC(lambda: mean[0]-mean[1])
        _sem = CC(lambda: math.sqrt(((n[0]-1)*(std[0]**2)+(n[1]-1)*(std[1]**2))*(1/n[0]+1/n[1])/(n[0]+n[1]-2)))
        t = CC(lambda: _mean/_sem)
        p = CC(lambda: st.t.cdf(t, n[0]+n[1]-2))
        p = CC(lambda a: 2*min(a, 1-a), p)

        diff = pd.DataFrame(
            {
                "Estimate" : CC(lambda: _mean) ,
                "Std. Error" : CC(lambda: _sem) ,
                "95% CI: Lower" : CC(lambda: st.t.ppf(0.025, n[0]+n[1]-2, _mean, _sem)) ,
                "95% CI: Upper" : CC(lambda: st.t.ppf(0.975, n[0]+n[1]-2, _mean, _sem)) ,
            }, index=["Difference"]
        )
        summary = pd.concat([summary, diff])

        result = pd.DataFrame(
            {
                "D.F." : CC(lambda: n[0]+n[1]-2) ,
                "t Statistic" : CC(lambda: t) ,
                "p-value" : CC(lambda: p)
            }, index=["Model"]
        )
    elif kind == "unequal variances":
        _mean = CC(lambda: mean[0]-mean[1])
        _sem = CC(lambda: math.sqrt(sem[0]**2+sem[1]**2))
        t = CC(lambda: _mean/_sem)
        df = CC(lambda: (sem[0]**2+sem[1]**2)**2/(sem[0]**4/(n[0]-1)+sem[1]**4/(n[1]-1)))
        p = CC(lambda: st.t.cdf(t, df))
        p = CC(lambda a: 2*min(a, 1-a), p)

        diff = pd.DataFrame(
            {
                "Estimate" : CC(lambda: _mean) ,
                "Std. Error" : CC(lambda: _sem) ,
                "95% CI: Lower" : CC(lambda: st.t.ppf(0.025, n[0]+n[1]-2, _mean, _sem)) ,
                "95% CI: Upper" : CC(lambda: st.t.ppf(0.975, n[0]+n[1]-2, _mean, _sem)) ,
            }, index=["Difference"]
        )
        summary = pd.concat([summary, diff])

        result = pd.DataFrame(
            {
                "D.F." : CC(lambda: df) ,
                "t Statistic" : CC(lambda: t) ,
                "p-value" : CC(lambda: p)
            }, index=["Model"]
        )
    else:
        return

    add_p(result)

    process(summary)
    process(result)

    return summary, result


def paired_t_test(data, variable, between, group, pair):

    process(data)
    data = data[list({variable, between, pair})].dropna()

    if str(data[variable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))
    if data[pair].nunique() > 2000:
        raise Warning("The nmuber of classes in column '{}' cannot > 2000.".format(pair))

    data = data[data[between].isin(group)]
    cross = pd.crosstab(index=data[pair], columns=data[between])
    for col in cross:
        cross = cross.drop(cross[cross[col] != 1].index)
    sub = cross.index.values.tolist()
    data = data[data[pair].isin(sub)]

    n, mean, std, sem = [None] * 2, [None] * 2, [None] * 2, [None] * 2
    for i, cat, in enumerate(group):
        n[i]    = CC(data[data[between]==cat][variable].dropna().count)
        mean[i] = CC(st.tmean, data[data[between]==cat][variable].dropna())
        std[i]  = CC(st.tstd, data[data[between]==cat][variable].dropna())
        sem[i]  = CC(st.tsem, data[data[between]==cat][variable].dropna())

    summary = pd.DataFrame(
        {
            "Estimate" : CC(lambda: mean) ,
            "Std. Error" : CC(lambda: sem) ,
            "95% CI: Lower" : [CC(lambda: st.t.ppf(0.025, n[i]-1, mean[i], sem[i])) for i in range(2)] ,
            "95% CI: Upper" : [CC(lambda: st.t.ppf(0.975, n[i]-1, mean[i], sem[i])) for i in range(2)] ,
        }, index=group
    )

    data_wide = pd.DataFrame(
        {
            "var_1" : data[data[between]==group[0]].sort_values(by=[pair])[variable].tolist() ,
            "var_2" : data[data[between]==group[1]].sort_values(by=[pair])[variable].tolist()
        }
    )

    diff = data_wide["var_1"] - data_wide["var_2"]
    diff = diff.dropna()

    _n = CC(lambda a: a.count(), diff.dropna())
    _mean = CC(st.tmean, diff.dropna())
    _sem = CC(st.tsem, diff.dropna())

    diff = pd.DataFrame(
        {
            "Estimate" : CC(lambda: _mean) ,
            "Std. Error" : CC(lambda: _sem) ,
            "95% CI: Lower" : CC(lambda: st.t.ppf(0.025, _n-1, _mean, _sem)) ,
            "95% CI: Upper" : CC(lambda: st.t.ppf(0.975, _n-1, _mean, _sem)) ,
        }, index=["Difference"]
    )
    summary = pd.concat([summary, diff])

    t = CC(lambda: _mean/_sem)
    p = CC(lambda: st.t.cdf(t, _n-1))
    p = CC(lambda a: 2*min(a, 1-a), p)
    result = pd.DataFrame(
        {
            "D.F." : CC(lambda: _n-1) ,
            "t Statistic" : CC(lambda: t) ,
            "p-value" : CC(lambda: p)
        }, index=["Model"]
    )
    add_p(result)

    process(summary)
    process(result)

    return summary, result


def pairwise_t_test(data, variable, between):

    process(data)
    data = data[list({variable, between})].dropna()

    if str(data[variable].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(variable))
    if data[between].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(between))

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
                "Count": CC(lambda: n),
                "Mean": CC(lambda: mean),
                "Std. Deviation": CC(lambda: std),
                "95% CI: Lower" : CC(lambda: st.t.ppf(0.025, n-1, mean, sem)) ,
                "95% CI: Upper" : CC(lambda: st.t.ppf(0.975, n-1, mean, sem)) ,
            }, index=[0]
        )
        summary = pd.concat([summary, temp], ignore_index=True)
    summary.index += 1
    result = pd.DataFrame()
    group = data[between].dropna().unique()
    df = CC(lambda: len(data[[variable, between]].dropna()) - len(group))
    corr = CC(lambda: len(group) * (len(group) - 1) / 2)

    formula = "Q('%s') ~ " % variable
    formula += "C(Q('%s'))" % between
    model = ols(formula, data=data).fit()
    anova = anova_lm(model)
    s = CC(lambda: math.sqrt(anova["mean_sq"][1]))

    for i in range(0, len(group)):
        for j in range(i+1, len(group)):
            n, mean, std = [None] * 2, [None] * 2, [None] * 2
            for k, cat, in enumerate([group[j], group[i]]):
                n[k]    = CC(data[data[between]==cat][variable].count)
                mean[k] = CC(st.tmean, data[data[between]==cat][variable].dropna())
                std[k]  = CC(st.tstd, data[data[between]==cat][variable].dropna())
            diff = CC(lambda: mean[0]-mean[1])
            sem = CC(lambda: s*math.sqrt(1/n[0]+1/n[1]))
            t = CC(lambda: diff/sem)
            p = CC(lambda: st.t.cdf(t, df))
            p = CC(lambda a: 2*min(a, 1-a), p)
            p = CC(lambda: p*corr)
            if p > 1:
                p = 1
            temp = pd.DataFrame(
                {
                    "Group 1" : CC(lambda: group[j]),
                    "Group 2" : CC(lambda: group[i]),
                    "Difference" : CC(lambda: diff),
                    "Std. Error" : CC(lambda: sem),
                    "t Statistic" : CC(lambda: t),
                    "p-value" : CC(lambda: p)
                }, index=[0]
            )
            result = pd.concat([result, temp], ignore_index=True)

    add_p(result)
    result.index += 1

    process(summary)
    process(result)

    return summary, result        



