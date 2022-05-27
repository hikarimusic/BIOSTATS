import pandas as pd
import numpy as np
from scipy import stats as st

def CC(fun, *args):
    try:
        return fun(*args)
    except:
        return np.nan

def numeral(data,variable):

    for col in data:
        try: 
            data[col] = data[col].astype('float64')
        except:
            pass

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

    for col in result:
        try: 
            result[col] = result[col].astype('float64')
        except:
            pass

    return result