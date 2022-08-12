import numpy as np

def _CC(fun, *args):
    try:
        return fun(*args)
    except:
        return np.nan

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


def _add_p(data):
    temp = [np.nan] * len(data)
    for i in range(len(data)):
        if data['p-value'][i] <= 0.05:
            temp[i] = "*"
        if data['p-value'][i] <= 0.01:
            temp[i] = "**"
        if data['p-value'][i] <= 0.001:
            temp[i] = "***"
    data[""] = temp