import os
import pandas as pd

def dataset(name=None):
    try:
        path = os.path.join(os.path.dirname(__file__), name)
        return pd.read_csv(path)
    except:
        return pd.DataFrame()