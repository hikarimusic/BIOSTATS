import matplotlib.pyplot as plt
import seaborn as sns

from biostats.model.util import _CC, _process, _add_p

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
        The categorical variable specifying groups to be plotted with different colors. Optional. 

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
        0    Adelie  Torgersen            39.1           18.7                181         3750    MALE
        1    Adelie  Torgersen            39.5           17.4                186         3800  FEMALE
        2    Adelie  Torgersen            40.3           18.0                195         3250  FEMALE
        3    Adelie  Torgersen             NaN            NaN               <NA>         <NA>     NaN
        4    Adelie  Torgersen            36.7           19.3                193         3450  FEMALE
        ..      ...        ...             ...            ...                ...          ...     ...
        339  Gentoo     Biscoe             NaN            NaN               <NA>         <NA>     NaN
        340  Gentoo     Biscoe            46.8           14.3                215         4850  FEMALE
        341  Gentoo     Biscoe            50.4           15.7                222         5750    MALE
        342  Gentoo     Biscoe            45.2           14.8                212         5200  FEMALE
        343  Gentoo     Biscoe            49.9           16.1                213         5400    MALE

        We want to visualize the distribution of *flipper_length_mm* in different *species*.

        >>> fig = bs.histogram(data=data, x="flipper_length_mm", band=10, color="species")
        >>> plt.show()

    '''

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data, num=[x], cat=[color])

    if str(data[x].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(x))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    fig, ax = plt.subplots()
    sns.histplot(data=data, x=x, bins=band, hue=color, ax=ax)
    
    return fig


def density_plot(data, x, smooth, color=None):
    '''
    Draw a density curve to show the distribution of a numeric variable.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column. 
    x : :py:class:`str`
        The numeric variable to be plotted.
    smooth : :py:class:`float` or :py:class:`int`
        The smoothing of the curve. Larger value with smoother curve.
    color : :py:class:`str`
        The categorical variable specifying groups to be plotted with different colors. Optional. 

    Returns
    -------
    fig : :py:class:`matplotlib.figure.Figure`
        The generated plot.

    See also
    --------
    histogram : Show the distribution by a histogram.
    density_plot_2D : Draw a 2 dimensional density plot from 2 numeric columns.

    Examples
    --------
    .. plot::

        >>> import biostats as bs
        >>> import matplotlib.pyplot as plt
        >>> data = bs.dataset("penguins.csv")
        >>> data
            species     island  bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g     sex
        0    Adelie  Torgersen            39.1           18.7                181         3750    MALE
        1    Adelie  Torgersen            39.5           17.4                186         3800  FEMALE
        2    Adelie  Torgersen            40.3           18.0                195         3250  FEMALE
        3    Adelie  Torgersen             NaN            NaN               <NA>         <NA>     NaN
        4    Adelie  Torgersen            36.7           19.3                193         3450  FEMALE
        ..      ...        ...             ...            ...                ...          ...     ...
        339  Gentoo     Biscoe             NaN            NaN               <NA>         <NA>     NaN
        340  Gentoo     Biscoe            46.8           14.3                215         4850  FEMALE
        341  Gentoo     Biscoe            50.4           15.7                222         5750    MALE
        342  Gentoo     Biscoe            45.2           14.8                212         5200  FEMALE
        343  Gentoo     Biscoe            49.9           16.1                213         5400    MALE

        We want to visualize the distribution of *flipper_length_mm* in different *species*.

        >>> fig = bs.density_plot(data=data, x="flipper_length_mm", smooth=1, color="species")
        >>> plt.show()

    '''

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data, num=[x], cat=[color])

    if str(data[x].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(x))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    fig, ax = plt.subplots()
    sns.kdeplot(data= data, x=x, bw_adjust=smooth, hue=color, ax=ax)
    
    return fig

def cumulative_plot(data, x, color=None):
    '''
    Draw a cumulative curve to show the distribution of a numeric variable.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column. 
    x : :py:class:`str`
        The numeric variable to be plotted.
    color : :py:class:`str`
        The categorical variable specifying groups to be plotted with different colors. Optional. 

    Returns
    -------
    fig : :py:class:`matplotlib.figure.Figure`
        The generated plot.

    See also
    --------
    density_plot: Show the distribution by a density curve.

    Examples
    --------
    .. plot::

        >>> import biostats as bs
        >>> import matplotlib.pyplot as plt
        >>> data = bs.dataset("penguins.csv")
        >>> data
            species     island  bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g     sex
        0    Adelie  Torgersen            39.1           18.7                181         3750    MALE
        1    Adelie  Torgersen            39.5           17.4                186         3800  FEMALE
        2    Adelie  Torgersen            40.3           18.0                195         3250  FEMALE
        3    Adelie  Torgersen             NaN            NaN               <NA>         <NA>     NaN
        4    Adelie  Torgersen            36.7           19.3                193         3450  FEMALE
        ..      ...        ...             ...            ...                ...          ...     ...
        339  Gentoo     Biscoe             NaN            NaN               <NA>         <NA>     NaN
        340  Gentoo     Biscoe            46.8           14.3                215         4850  FEMALE
        341  Gentoo     Biscoe            50.4           15.7                222         5750    MALE
        342  Gentoo     Biscoe            45.2           14.8                212         5200  FEMALE
        343  Gentoo     Biscoe            49.9           16.1                213         5400    MALE

        We want to visualize the cumulative distribution of *flipper_length_mm* in different *species*.

        >>> fig = bs.density_plot(data=data, x="flipper_length_mm", smooth=1, color="species")
        >>> plt.show()

    '''

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data, num=[x], cat=[color])

    if str(data[x].dtypes) not in ("float64", "Int64"):
        raise Warning("The column '{}' must be numeric".format(x))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    fig, ax = plt.subplots()
    sns.ecdfplot(data= data, x=x, hue=color, ax=ax)
    
    return fig

def histogram_2D(data, x, y, color=None):
    '''
    Draw a 2D histogram to show the distribution of two numeric variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two numeric columns. 
    x : :py:class:`str`
        The numeric variable to be plotted in x-axis.
    y : :py:class:`str`
        The numeric variable to be plotted in y-axis.
    color : :py:class:`str`
        The categorical variable specifying groups to be plotted with different colors. Optional. 

    Returns
    -------
    fig : :py:class:`matplotlib.figure.Figure`
        The generated plot.

    See also
    --------
    density_plot_2D : Show the 2D distribution by density curves.
    histogram : Draw a histogram to show the distribution of a numeric variable.

    Examples
    --------
    .. plot::

        >>> import biostats as bs
        >>> import matplotlib.pyplot as plt
        >>> data = bs.dataset("penguins.csv")
        >>> data
            species     island  bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g     sex
        0    Adelie  Torgersen            39.1           18.7                181         3750    MALE
        1    Adelie  Torgersen            39.5           17.4                186         3800  FEMALE
        2    Adelie  Torgersen            40.3           18.0                195         3250  FEMALE
        3    Adelie  Torgersen             NaN            NaN               <NA>         <NA>     NaN
        4    Adelie  Torgersen            36.7           19.3                193         3450  FEMALE
        ..      ...        ...             ...            ...                ...          ...     ...
        339  Gentoo     Biscoe             NaN            NaN               <NA>         <NA>     NaN
        340  Gentoo     Biscoe            46.8           14.3                215         4850  FEMALE
        341  Gentoo     Biscoe            50.4           15.7                222         5750    MALE
        342  Gentoo     Biscoe            45.2           14.8                212         5200  FEMALE
        343  Gentoo     Biscoe            49.9           16.1                213         5400    MALE

        We want to visualize the 2D distribution of *bill_depth_mm* and *body_mass_g* in different *species*.

        >>> fig = bs.histogram_2D(data=data, x="bill_depth_mm", y="body_mass_g", color="species")
        >>> plt.show()

    '''

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
    sns.histplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig

def density_plot_2D(data, x, y, color=None):
    '''
    Draw a 2D density plot to show the distribution of two numeric variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two numeric columns. 
    x : :py:class:`str`
        The numeric variable to be plotted in x-axis.
    y : :py:class:`str`
        The numeric variable to be plotted in y-axis.
    color : :py:class:`str`
        The categorical variable specifying groups to be plotted with different colors. Optional. 

    Returns
    -------
    fig : :py:class:`matplotlib.figure.Figure`
        The generated plot.

    See also
    --------
    histogram_2D : Show the 2D distribution by a histogram.
    density_plot : Draw a density curve to show the distribution of a numeric variable.

    Examples
    --------
    .. plot::

        >>> import biostats as bs
        >>> import matplotlib.pyplot as plt
        >>> data = bs.dataset("penguins.csv")
        >>> data
            species     island  bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g     sex
        0    Adelie  Torgersen            39.1           18.7                181         3750    MALE
        1    Adelie  Torgersen            39.5           17.4                186         3800  FEMALE
        2    Adelie  Torgersen            40.3           18.0                195         3250  FEMALE
        3    Adelie  Torgersen             NaN            NaN               <NA>         <NA>     NaN
        4    Adelie  Torgersen            36.7           19.3                193         3450  FEMALE
        ..      ...        ...             ...            ...                ...          ...     ...
        339  Gentoo     Biscoe             NaN            NaN               <NA>         <NA>     NaN
        340  Gentoo     Biscoe            46.8           14.3                215         4850  FEMALE
        341  Gentoo     Biscoe            50.4           15.7                222         5750    MALE
        342  Gentoo     Biscoe            45.2           14.8                212         5200  FEMALE
        343  Gentoo     Biscoe            49.9           16.1                213         5400    MALE

        We want to visualize the 2D distribution of *bill_depth_mm* and *body_mass_g* in different *species*.

        >>> fig = bs.density_plot_2D(data=data, x="bill_depth_mm", y="body_mass_g", color="species")
        >>> plt.show()

    '''

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
    sns.kdeplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig
