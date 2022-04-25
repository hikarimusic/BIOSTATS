import numpy as np
import pandas as pd

from scipy.stats import chi2_contingency

def chi_square_test(data=None, first=None, second=None, summary=None):

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
    
    if summary == 1:
        return table
    else:
        return result