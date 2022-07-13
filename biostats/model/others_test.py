import pandas as pd
import numpy as np
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

def linear_discriminant_analysis(data, x, y, predict=None):

    process(data)

    data = data.dropna()

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
    