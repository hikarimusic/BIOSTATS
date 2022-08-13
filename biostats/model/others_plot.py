import matplotlib.pyplot as plt
import seaborn as sns
from factor_analyzer import FactorAnalyzer
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from biostats.model.util import _CC, _process, _add_p

def heatmap(data, x, y, value):
    '''
    Draw a heat map to show the relation between two categorical variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and two categorical columns. 
    x : :py:class:`str`
        The categorical variable to be plotted in x-axis.
    y : :py:class:`str`
        The categorical variable to be plotted in y-axis.
    value : :py:class:`str`
        The numeric variable to be plotted with different colors.

    Returns
    -------
    fig : :py:class:`matplotlib.figure.Figure`
        The generated plot.

    See also
    --------
    histogram_2D : Draw a 2D histogram to show the distribution of two numeric variables.

    Examples
    --------
    .. plot::

        >>> import biostats as bs
        >>> import matplotlib.pyplot as plt
        >>> data = bs.dataset("flights.csv")
        >>> data
             year      month  passengers
        0    1949    January         112
        1    1949   February         118
        2    1949      March         132
        3    1949      April         129
        4    1949        May         121
        ..    ...        ...         ...
        139  1960     August         606
        140  1960  September         508
        141  1960    October         461
        142  1960   November         390
        143  1960   December         432

        We want to visualize the relation between *year* and *month* by examining *passengers*.

        >>> fig = bs.heatmap(data=data, x="year", y="month", value="passengers")
        >>> plt.show()

    '''

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data, num=[value], cat=[x, y])

    if data[x].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_1))
    if data[y].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(variable_2))
    if str(data[value].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(value))

    fig, ax = plt.subplots(figsize=(6,6))
    sns.heatmap(data.pivot_table(index=y, columns=x, values=value, sort=False), ax=ax)
        
    return fig

def fa_plot(data, x, factors, color=None):

    sns.set_theme()
    data = data.dropna()
    _process(data, num=x, cat=[color])

    for var in x:
        if str(data[var].dtypes) not in ("float64", "Int64"):
            raise Warning("The column '{}' must be numeric".format(var))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    #for var in x:
    #    data[var] = (data[var] - data[var].mean()) / data[var].std()

    clf = FactorAnalyzer(n_factors=factors, rotation='varimax')
    clf.fit(data[x])

    fa = clf.transform(data[x])
    
    if fa.shape[1] < 2:
        data["f_1"] = fa[:,0]
        fig, ax = plt.subplots()
        sns.stripplot(data=data, x="f_1", y=color, hue=color, ax=ax)
        ax.set(xlabel="Factor 1")
    else:
        data["f_1"] = fa[:,0]
        data["f_2"] = fa[:,1]
        fig, ax = plt.subplots()
        sns.scatterplot(data=data, x="f_1", y="f_2", hue=color, ax=ax)
        ax.set(xlabel="Factor 1")
        ax.set(ylabel="Factor 2")
        
    return fig


def pca_plot(data, x, color=None):

    sns.set_theme()
    data = data.dropna()
    _process(data, num=x, cat=[color])

    for var in x:
        if str(data[var].dtypes) not in ("float64", "Int64"):
            raise Warning("The column '{}' must be numeric".format(var))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))
            
    #for var in x:
    #    data[var] = (data[var] - data[var].mean()) / data[var].std()

    clf = PCA()
    clf.fit(data[x])

    pca = clf.transform(data[x])
    
    if pca.shape[1] < 2:
        data["pc_1"] = pca[:,0]
        fig, ax = plt.subplots()
        sns.stripplot(data=data, x="pc_1", y=color, hue=color, ax=ax)
        ax.set(xlabel="PC 1")
    else:
        data["pc_1"] = pca[:,0]
        data["pc_2"] = pca[:,1]
        fig, ax = plt.subplots()
        sns.scatterplot(data=data, x="pc_1", y="pc_2", hue=color, ax=ax)
        ax.set(xlabel="PC 1 ({}%)".format(round(clf.explained_variance_ratio_[0]*100,1)))
        ax.set(ylabel="PC 2 ({}%)".format(round(clf.explained_variance_ratio_[1]*100,1)))
        
    return fig


def lda_plot(data, x, y):

    sns.set_theme()
    data = data.dropna()
    _process(data, num=x, cat=[y])

    for var in x:
        if str(data[var].dtypes) not in ("float64", "Int64"):
            raise Warning("The column '{}' must be numeric".format(var))
    if data[y].nunique() > 20:
        raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(y))

    clf = LinearDiscriminantAnalysis()
    clf.fit(data[x], data[y])

    lda = clf.transform(data[x])
    
    if lda.shape[1] < 2:
        data["ld_1"] = lda[:,0]
        fig, ax = plt.subplots()
        sns.stripplot(data=data, x="ld_1", y=y, hue=y, ax=ax)
        ax.set(xlabel="LD 1")
    else:
        data["ld_1"] = lda[:,0]
        data["ld_2"] = lda[:,1]
        fig, ax = plt.subplots()
        sns.scatterplot(data=data, x="ld_1", y="ld_2", hue=y, ax=ax)
        ax.set(xlabel="LD 1 ({}%)".format(round(clf.explained_variance_ratio_[0]*100,1)))
        ax.set(ylabel="LD 2 ({}%)".format(round(clf.explained_variance_ratio_[1]*100,1)))
        
    return fig
