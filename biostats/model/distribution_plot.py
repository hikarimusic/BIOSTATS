import matplotlib.pyplot as plt
import seaborn as sns

def process(data):
    for col in data:
        try: 
            data[col] = data[col].astype('float64')
        except:
            pass  
    data.columns = data.columns.map(str)
    data.index = data.index.map(str)

def histogram(data, x, band, color=None):

    sns.set_theme()
    process(data)

    if str(data[x].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(x))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    fig, ax = plt.subplots()
    sns.histplot(data=data, x=x, bins=band, hue=color, ax=ax)
        
    return fig


def density_plot(data, x, smooth, color=None):

    sns.set_theme()
    process(data)

    if str(data[x].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(x))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    fig, ax = plt.subplots()
    sns.kdeplot(data= data, x=x, bw_adjust=smooth, hue=color, ax=ax)
    
    return fig

def cumulative_plot(data, x, color=None):

    sns.set_theme()
    process(data)

    if str(data[x].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(x))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    fig, ax = plt.subplots()
    sns.ecdfplot(data= data, x=x, hue=color, ax=ax)
    
    return fig

def histogram_2D(data, x, y, color=None):

    sns.set_theme()
    process(data)

    if str(data[x].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(x))
    if str(data[y].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(y))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    fig, ax = plt.subplots()
    sns.histplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig

def density_plot_2D(data, x, y, color=None):

    sns.set_theme()
    process(data)

    if str(data[x].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(x))
    if str(data[y].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(y))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))
            
    fig, ax = plt.subplots()
    sns.kdeplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig
