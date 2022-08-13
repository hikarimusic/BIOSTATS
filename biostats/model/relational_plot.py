import matplotlib.pyplot as plt
import seaborn as sns

from biostats.model.util import _CC, _process, _add_p

def scatter_plot(data, x, y, color=None):
    '''
    Draw a scatter plot to show the relation between two numeric variables.

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
    line_plot : Draw a line plot to show the relation between two numeric variables.
    regression_plot : Draw a regression line to show the relation between two numeric variables.

    Examples
    --------
    .. plot::

        >>> import biostats as bs
        >>> import matplotlib.pyplot as plt
        >>> data = bs.dataset("tips.csv")
        >>> data
             total_bill   tip     sex smoker   day    time  size
        0         16.99  1.01  Female     No   Sun  Dinner     2
        1         10.34  1.66    Male     No   Sun  Dinner     3
        2         21.01  3.50    Male     No   Sun  Dinner     3
        3         23.68  3.31    Male     No   Sun  Dinner     2
        4         24.59  3.61  Female     No   Sun  Dinner     4
        ..          ...   ...     ...    ...   ...     ...   ...
        239       29.03  5.92    Male     No   Sat  Dinner     3
        240       27.18  2.00  Female    Yes   Sat  Dinner     2
        241       22.67  2.00    Male    Yes   Sat  Dinner     2
        242       17.82  1.75    Male     No   Sat  Dinner     2
        243       18.78  3.00  Female     No  Thur  Dinner     2

        We want to visualize the relation between *total_bill* and *tip*.

        >>> fig = bs.scatter_plot(data=data, x="total_bill", y="tip", color="day")
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
    sns.scatterplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig

def line_plot(data, x, y, color=None):
    '''
    Draw a line plot to show the relation between two numeric variables.

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
    scatter_plot : Draw a scatter plot to show the relation between two numeric variables.
    regression_plot : Draw a regression line to show the relation between two numeric variables.

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

        We want to visualize the relation between *year* and *passengers*.

        >>> fig = bs.line_plot(data=data, x="year", y="passengers", color="month")
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
    sns.lineplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig

def regression_plot(data, x, y):
    '''
    Draw a regression line to show the relation between two numeric variables.

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
    scatter_plot : Draw a scatter plot to show the relation between two numeric variables.
    line_plot : Draw a line plot to show the relation between two numeric variables.

    Examples
    --------
    .. plot::

        >>> import biostats as bs
        >>> import matplotlib.pyplot as plt
        >>> data = bs.dataset("tips.csv")
        >>> data
             total_bill   tip     sex smoker   day    time  size
        0         16.99  1.01  Female     No   Sun  Dinner     2
        1         10.34  1.66    Male     No   Sun  Dinner     3
        2         21.01  3.50    Male     No   Sun  Dinner     3
        3         23.68  3.31    Male     No   Sun  Dinner     2
        4         24.59  3.61  Female     No   Sun  Dinner     4
        ..          ...   ...     ...    ...   ...     ...   ...
        239       29.03  5.92    Male     No   Sat  Dinner     3
        240       27.18  2.00  Female    Yes   Sat  Dinner     2
        241       22.67  2.00    Male    Yes   Sat  Dinner     2
        242       17.82  1.75    Male     No   Sat  Dinner     2
        243       18.78  3.00  Female     No  Thur  Dinner     2

        We want to visualize the relation between *total_bill* and *tip*.

        >>> fig = bs.regression_plot(data=data, x="total_bill", y="tip")
        >>> plt.show()

    '''

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