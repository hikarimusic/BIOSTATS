import numpy as np
import pandas as pd

from scipy.stats import chisquare, chi2_contingency

def chi_square_independence(data, first, second, summary=None):

    table = pd.crosstab(index=data[first], columns=data[second])
    table.index.name = None
    index_change = {}
    for index in table.index:
        changed = "{}({})".format(first, index)
        index_change[index] = changed
    table =  table.rename(index=index_change)
    table.columns.name = None
    columns_change = {}
    for columns in table.columns:
        changed = "{}({})".format(second, columns)
        columns_change[columns] = changed
    table =  table.rename(columns=columns_change)

    chi2, p, df, ex = chi2_contingency(table, False)
    chi2_, p_, df_, ex_, = chi2_contingency(table, True)
    result = pd.DataFrame(
        {
            "Chi_Square": [chi2, chi2_],
            "df": [df, df_],
            "p-value": [p, p_]
        }, index=["Normal", "Corrected"]
    )
    
    if summary:
        return table
    else:
        return result

def chi_square_fit(data, target, expected, summary=None):
    
    Observed = data[target].value_counts().to_numpy()
    Index = data[target].value_counts().index
    Expected = []
    for var in Index:
        Expected.append(expected[var])
    Expected = np.array(Expected) / np.sum(np.array(Expected)) * np.sum(Observed)
    table = pd.DataFrame(
        {
            "Observed": Observed,
            "Expected": Expected
        }, index = Index
    ).T
    table = table[expected.keys()]
    columns_change = {}
    for columns in table.columns:
        changed = "{}({})".format(target, columns)
        columns_change[columns] = changed
    table = table.rename(columns=columns_change)

    chi2, p = chisquare(Observed, f_exp=Expected)

    result = pd.DataFrame(
        {
            "Chi-Square": chi2,
            "df": Observed.size-1, 
            "p-value": p
        }, index=["Fit"]
    )

    if summary:
        return table
    else:
        return result