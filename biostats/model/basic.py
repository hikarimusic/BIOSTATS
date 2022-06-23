import pandas as pd
import numpy as np
from scipy import stats as st
import math

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

def numeral(data, variable):

    process(data)

    index = ["Count", "Mean", "Median", "Geometric Mean", "Harmonic Mean", "Mode"]
    index += ["", "Variance", "Std. Deviation", "Coef. Variation", "(Population) Variance", "(Population) Std.Dev"]
    index += ["", "Minimum", "25% Percentile", "50% Percentile", "75% Percentile", "Maximum", "Range", "Interquartile Range"]
    index += ["", "Std. Error", "95% CI: Lower", "95% CI: Upper", "(One-Tail) 95% CI: Lower", "(One-Tail) 95% CI: Upper"]
    result = pd.DataFrame(index=index)

    for var in variable:
        result[var] = [
            CC(data[var].count) ,
            CC(st.tmean, data[var].dropna()) ,
            CC(np.median, data[var].dropna()) ,
            CC(st.gmean, data[var].dropna()) ,
            CC(st.hmean, data[var].dropna()) ,
            CC(lambda a: st.mode(a)[0][0], data[var].dropna()) ,
            np.nan ,
            CC(st.tvar, data[var].dropna()) ,
            CC(st.tstd, data[var].dropna()) ,
            CC(lambda a: st.tstd(a)/st.tmean(a), data[var].dropna()) ,
            CC(np.var, data[var].dropna()) ,
            CC(np.std, data[var].dropna()) ,
            np.nan ,
            CC(np.percentile, data[var].dropna(), 0) ,
            CC(np.percentile, data[var].dropna(), 25) ,
            CC(np.percentile, data[var].dropna(), 50) ,
            CC(np.percentile, data[var].dropna(), 75) ,
            CC(np.percentile, data[var].dropna(), 100) ,
            CC(lambda a: np.percentile(a,100)-np.percentile(a,0), data[var].dropna()) ,
            CC(lambda a: np.percentile(a,75)-np.percentile(a,25), data[var].dropna()) ,
            np.nan ,
            CC(st.tsem, data[var].dropna()) ,
            CC(lambda a: st.t.ppf(0.025, a.count()-1, st.tmean(a), st.tsem(a)), data[var].dropna()) ,
            CC(lambda a: st.t.ppf(0.975, a.count()-1, st.tmean(a), st.tsem(a)), data[var].dropna()) ,
            CC(lambda a: st.t.ppf(0.050, a.count()-1, st.tmean(a), st.tsem(a)), data[var].dropna()) ,
            CC(lambda a: st.t.ppf(0.950, a.count()-1, st.tmean(a), st.tsem(a)), data[var].dropna()) ,
        ]

    process(result)

    return result


def numeral_grouped(data, variable, group):

    process(data)

    index = ["Count", "Mean", "Median", "Geometric Mean", "Harmonic Mean", "Mode"]
    index += ["", "Variance", "Std. Deviation", "Coef. Variation", "(Population) Variance", "(Population) Std.Dev"]
    index += ["", "Minimum", "25% Percentile", "50% Percentile", "75% Percentile", "Maximum", "Range", "Interquartile Range"]
    index += ["", "Std. Error", "95% CI: Lower", "95% CI: Upper", "(One-Tail) 95% CI: Lower", "(One-Tail) 95% CI: Upper"]
    result = pd.DataFrame(index=index)

    for cat in data[group].dropna().unique():
        result[cat] = [
            CC(data[data[group]==cat][variable].count) ,
            CC(st.tmean, data[data[group]==cat][variable].dropna()) ,
            CC(np.median, data[data[group]==cat][variable].dropna()) ,
            CC(st.gmean, data[data[group]==cat][variable].dropna()) ,
            CC(st.hmean, data[data[group]==cat][variable].dropna()) ,
            CC(lambda a: st.mode(a)[0][0], data[data[group]==cat][variable].dropna()) ,
            np.nan ,
            CC(st.tvar, data[data[group]==cat][variable].dropna()) ,
            CC(st.tstd, data[data[group]==cat][variable].dropna()) ,
            CC(lambda a: st.tstd(a)/st.tmean(a), data[data[group]==cat][variable].dropna()) ,
            CC(np.var, data[data[group]==cat][variable].dropna()) ,
            CC(np.std, data[data[group]==cat][variable].dropna()) ,
            np.nan ,
            CC(np.percentile, data[data[group]==cat][variable].dropna(), 0) ,
            CC(np.percentile, data[data[group]==cat][variable].dropna(), 25) ,
            CC(np.percentile, data[data[group]==cat][variable].dropna(), 50) ,
            CC(np.percentile, data[data[group]==cat][variable].dropna(), 75) ,
            CC(np.percentile, data[data[group]==cat][variable].dropna(), 100) ,
            CC(lambda a: np.percentile(a,100)-np.percentile(a,0), data[data[group]==cat][variable].dropna()) ,
            CC(lambda a: np.percentile(a,75)-np.percentile(a,25), data[data[group]==cat][variable].dropna()) ,
            np.nan ,
            CC(st.tsem, data[data[group]==cat][variable].dropna()) ,
            CC(lambda a: st.t.ppf(0.025, a.count()-1, st.tmean(a), st.tsem(a)), data[data[group]==cat][variable].dropna()) ,
            CC(lambda a: st.t.ppf(0.975, a.count()-1, st.tmean(a), st.tsem(a)), data[data[group]==cat][variable].dropna()) ,
            CC(lambda a: st.t.ppf(0.050, a.count()-1, st.tmean(a), st.tsem(a)), data[data[group]==cat][variable].dropna()) ,
            CC(lambda a: st.t.ppf(0.950, a.count()-1, st.tmean(a), st.tsem(a)), data[data[group]==cat][variable].dropna()) ,
        ]    

    process(result)

    return result


def categorical(data, variable):

    process(data)

    cat = data.groupby(variable, sort=False)[variable].groups.keys()
    cnt = []
    prop = []
    CI_low = []
    CI_high = []
    for var in cat:
        cnt.append(CC(lambda: data[variable].value_counts()[var]))
    n = sum(cnt)
    for x in cnt:
        prop.append(CC(lambda: x / n))
        p = x / n
        ser = math.sqrt(p * (1 - p) / n)
        CI_low.append(CC(lambda: p + st.norm.ppf(0.025) * ser))
        CI_high.append(CC(lambda: p + st.norm.ppf(0.975) * ser))

    result = pd.DataFrame(
        {
            "Count" : cnt, 
            "Proportion"  : prop,
            "95% CI: Lower" : CI_low,
            "95% CI: Upper" : CI_high
        }, index=cat
    )

    process(result)

    return result


def contingency(data, variable_1, variable_2, kind="Count"):

    process(data)

    result = pd.crosstab(index=data[variable_1], columns=data[variable_2])
    result.index.name = None
    result.columns.name = None

    if kind == "Vertical":
        col_sum = result.sum(axis=0)
        for i in range(result.shape[0]):
            for j in range(result.shape[1]):
                result.iat[i,j] /= col_sum[j]

    if kind == "Horizontal":
        col_sum = result.sum(axis=1)
        for i in range(result.shape[0]):
            for j in range(result.shape[1]):
                result.iat[i,j] /= col_sum[i]

    if kind == "Overall":
        _sum = result.to_numpy().sum()
        for i in range(result.shape[0]):
            for j in range(result.shape[1]):
                result.iat[i,j] /= _sum

    process(result)

    return result