import matplotlib.pyplot as plt
import seaborn as sns

from biostats.model.util import _CC, _process, _add_p

def count_plot(data, x, color=None):

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data, cat=[x, color])

    if data[x].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(x))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    fig, ax = plt.subplots()
    sns.countplot(data=data, x=x, hue=color, ax=ax)
        
    return fig

def strip_plot(data, x, y, color=None):

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data, num=[y], cat=[x, color])

    if data[x].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(x))
    if str(data[y].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(y))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))
            
    fig, ax = plt.subplots()
    sns.stripplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig

def swarm_plot(data, x, y, color=None):

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data, num=[y], cat=[x, color])

    if data[x].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(x))
    if str(data[y].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(y))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    fig, ax = plt.subplots()
    sns.swarmplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig

def box_plot(data, x, y, color=None):

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data, num=[y], cat=[x, color])

    if data[x].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(x))
    if str(data[y].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(y))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    fig, ax = plt.subplots()
    sns.boxplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig

def boxen_plot(data, x, y, color=None):

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data, num=[y], cat=[x, color])

    if data[x].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(x))
    if str(data[y].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(y))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    fig, ax = plt.subplots()
    sns.boxenplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig

def violin_plot(data, x, y, color=None):

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data, num=[y], cat=[x, color])

    if data[x].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(x))
    if str(data[y].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(y))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    fig, ax = plt.subplots()
    sns.violinplot(data=data, x=x, y=y, hue=color, ax=ax)

    return fig

def bar_plot(data, x, y, color=None):

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data, num=[y], cat=[x, color])
    
    if data[x].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(x))
    if str(data[y].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(y))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))
            
    fig, ax = plt.subplots()
    sns.barplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig