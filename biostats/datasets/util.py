import os
import pandas as pd

def _process(data, num=[], cat=[]):
    for col in data:
        if col in num:
            try: 
                data[col] = data[col].astype('float64')
            except:
                pass 
        elif col in cat:
            try: 
                data[col] = data[col].astype('object')
            except:
                pass 
        else:
            try: 
                data[col] = data[col].astype('float64')
                try: 
                    data[col] = data[col].astype('Int64')
                except:
                    pass
            except:
                data[col] = data[col].astype('object')
    data.columns = data.columns.map(str)
    data.index = data.index.map(str)

def dataset(name=None):
    try:
        path = os.path.join(os.path.dirname(__file__), name)
        data = pd.read_csv(path, dtype=object)
        _process(data)
        return data
    except:
        return pd.DataFrame()