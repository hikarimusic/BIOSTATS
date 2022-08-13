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
    '''
    Load the example datasets of BIOSTATS.

    Parameters
    ----------
    name : :py:class:`str`
        The name of the dataset.

    Returns
    -------
    data : :py:class:`pandas.DataFrame`
        The dataset.

    Notes
    -----
    The names of the example datasets are *function_name.csv*. There are also some famous datasets, such as *penguins.csv*, *iris.csv*, *tips.csv*, *titanic.csv*, and *flights.csv*.

    Examples
    --------
    >>> import biostats as bs
    >>> data = bs.dataset("one_way_anova.csv")
    >>> data
        Length    Location
    0   0.0571   Tillamook
    1   0.0813   Tillamook
    2   0.0831   Tillamook
    3   0.0976   Tillamook
    4   0.0817   Tillamook
    5   0.0859   Tillamook
    6   0.0735   Tillamook
    7   0.0659   Tillamook
    8   0.0923   Tillamook
    9   0.0836   Tillamook
    10  0.0873     Newport
    11  0.0662     Newport
    12  0.0672     Newport
    13  0.0819     Newport
    14  0.0749     Newport
    15  0.0649     Newport
    16  0.0835     Newport
    17  0.0725     Newport
    18  0.0974  Petersburg
    19  0.1352  Petersburg
    20  0.0817  Petersburg
    21  0.1016  Petersburg
    22  0.0968  Petersburg
    23  0.1064  Petersburg
    24  0.1050  Petersburg
    25  0.1033     Magadan
    26  0.0915     Magadan
    27  0.0781     Magadan
    28  0.0685     Magadan
    29  0.0677     Magadan
    30  0.0697     Magadan
    31  0.0764     Magadan
    32  0.0689     Magadan
    33  0.0703   Tvarminne
    34  0.1026   Tvarminne
    35  0.0956   Tvarminne
    36  0.0973   Tvarminne
    37  0.1039   Tvarminne
    38  0.1045   Tvarminne

    '''

    try:
        path = os.path.join(os.path.dirname(__file__), name)
        data = pd.read_csv(path, dtype=object)
        _process(data)
        return data
    except:
        return pd.DataFrame()