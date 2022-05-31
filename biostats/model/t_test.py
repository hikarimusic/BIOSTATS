import pandas as pd
import numpy as np
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


def one_sample_t_test(data, variable, expect, kind="two-side"):

    process(data)

    n = CC(lambda a: a.count(), data[variable].dropna())
    mean = CC(st.tmean, data[variable].dropna())
    sem = CC(st.tsem, data[variable].dropna())

    if kind == "two-side":
        summary = pd.DataFrame(
            {
                "Count" : n ,
                "Mean" : mean ,
                "95% CI: Lower" : CC(lambda a: st.t.ppf(0.025, n-1, mean, sem), 0) ,
                "95% CI: Upper" : CC(lambda a: st.t.ppf(0.975, n-1, mean, sem), 0) ,
                "Expect" : expect
            }, index=[variable]
        )
        t = CC(lambda a: (mean-expect)/sem, 0)
        p = CC(lambda a: st.t.cdf(t, n-1), 0)
        p = CC(lambda a: 2*min(a, 1-a), p)
        result = pd.DataFrame(
            {
                "D.F." : n-1 ,
                "t Statistic" : t ,
                "p-value" : p
            }, index=[variable]
        )
    elif kind == "greater":
        summary = pd.DataFrame(
            {
                "Count" : n ,
                "Mean" : mean ,
                "95% CI: Lower" : CC(lambda a: st.t.ppf(0.05, n-1, mean, sem), 0) ,
                "95% CI: Upper" : "Inf" ,
                "Expect" : expect
            }, index=[variable]
        )
        t = CC(lambda a: (mean-expect)/sem, 0)
        p = CC(lambda a: st.t.cdf(t, n-1), 0)
        p = CC(lambda a: 1-a, p)
        result = pd.DataFrame(
            {
                "D.F." : n-1 ,
                "t Statistic" : t ,
                "p-value" : p
            }, index=[variable]
        )
    elif kind == "less":
        summary = pd.DataFrame(
            {
                "Count" : n ,
                "Mean" : mean ,
                "95% CI: Lower" : "-Inf" ,
                "95% CI: Upper" : CC(lambda a: st.t.ppf(0.95, n-1, mean, sem), 0) ,
                "Expect" : expect
            }, index=[variable]
        )
        t = CC(lambda a: (mean-expect)/sem, 0)
        p = CC(lambda a: st.t.cdf(t, n-1), 0)
        result = pd.DataFrame(
            {
                "D.F." : n-1 ,
                "t Statistic" : t ,
                "p-value" : p
            }, index=[variable]
        )
    else:
        return

    add_p(result)

    process(summary)
    process(result)

    return summary, result

