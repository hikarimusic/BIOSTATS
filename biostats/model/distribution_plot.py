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

    '''
    Draw a histogram to show the distribution of a numeric variable.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column. 
    x : :py:class:`str`
        The numeric variable to be plotted.
    band : :py:class:`int`
        The number of bands in the histogram.
    color : :py:class:`str`
        When specified, histograms with different colors will be drawn on the same plot for each group of the *color* variable.

    Returns
    -------
    fig : :py:class:`matplotlib.figure.Figure`
        The generated plot.

    See also
    --------
    density_plot : Show the distribution by a density curve.
    histogram_2D : Draw a 2 dimensional histogram from 2 numeric columns.

    Examples
    --------
    .. plot::

        >>> import biostats as bs
        >>> import matplotlib.pyplot as plt
        >>> data = bs.dataset("penguins.csv")
        >>> data
            species     island  bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g     sex
        0    Adelie  Torgersen            39.1           18.7              181.0       3750.0    MALE
        1    Adelie  Torgersen            39.5           17.4              186.0       3800.0  FEMALE
        2    Adelie  Torgersen            40.3           18.0              195.0       3250.0  FEMALE
        3    Adelie  Torgersen             NaN            NaN                NaN          NaN     NaN
        4    Adelie  Torgersen            36.7           19.3              193.0       3450.0  FEMALE
        ..      ...        ...             ...            ...                ...          ...     ...
        339  Gentoo     Biscoe             NaN            NaN                NaN          NaN     NaN
        340  Gentoo     Biscoe            46.8           14.3              215.0       4850.0  FEMALE
        341  Gentoo     Biscoe            50.4           15.7              222.0       5750.0    MALE
        342  Gentoo     Biscoe            45.2           14.8              212.0       5200.0  FEMALE
        343  Gentoo     Biscoe            49.9           16.1              213.0       5400.0    MALE

        We want to visualize the distribution of *flipper_length_mm* within different *species*.

        >>> fig = bs.histogram(data=data, x="flipper_length_mm", band=10, color="species")
        >>> plt.show()

    '''

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
