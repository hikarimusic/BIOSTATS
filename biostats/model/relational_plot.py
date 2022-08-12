import matplotlib.pyplot as plt
import seaborn as sns

from biostats.model.util import _CC, _process, _add_p

def scatter_plot(data, x, y, color=None):

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data, num=[x, y], cat=[color])

    if str(data[x].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(x))
    if str(data[y].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(y))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    fig, ax = plt.subplots()
    sns.scatterplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig

def line_plot(data, x, y, color=None):

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data, num=[x, y], cat=[color])

    if str(data[x].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(x))
    if str(data[y].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(y))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    fig, ax = plt.subplots()
    sns.lineplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig

def regression_plot(data, x, y):

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data, num=[x, y])
    
    if str(data[x].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(x))
    if str(data[y].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(y))

    fig, ax = plt.subplots()
    sns.regplot(data=data, x=x, y=y, ax=ax)
        
    return fig