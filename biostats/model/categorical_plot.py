import matplotlib.pyplot as plt
import seaborn as sns

from biostats.model.util import _CC, _process, _add_p

def count_plot(data, x, color=None):
    '''
    Draw a bar plot to show the counts of groups in a categorical variable.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one categorical column. 
    x : :py:class:`str`
        The categorical variable to be plotted.
    color : :py:class:`str`
        The categorical variable specifying groups to be plotted with different colors. Optional. 

    Returns
    -------
    fig : :py:class:`matplotlib.figure.Figure`
        The generated plot.

    See also
    --------
    bar_plot : Draw a bar plot to show the difference between groups in a categorical variable.

    Examples
    --------
    .. plot::

        >>> import biostats as bs
        >>> import matplotlib.pyplot as plt
        >>> data = bs.dataset("titanic.csv")
        >>> data
             survived  pclass     sex   age  sibsp  parch     fare embarked   class    who adult_male deck  embark_town alive  alone
        0           0       3    male  22.0      1      0   7.2500        S   Third    man       True  NaN  Southampton    no  False
        1           1       1  female  38.0      1      0  71.2833        C   First  woman      False    C    Cherbourg   yes  False
        2           1       3  female  26.0      0      0   7.9250        S   Third  woman      False  NaN  Southampton   yes   True
        3           1       1  female  35.0      1      0  53.1000        S   First  woman      False    C  Southampton   yes  False
        4           0       3    male  35.0      0      0   8.0500        S   Third    man       True  NaN  Southampton    no   True
        ..        ...     ...     ...   ...    ...    ...      ...      ...     ...    ...        ...  ...          ...   ...    ...
        886         0       2    male  27.0      0      0  13.0000        S  Second    man       True  NaN  Southampton    no   True
        887         1       1  female  19.0      0      0  30.0000        S   First  woman      False    B  Southampton   yes   True
        888         0       3  female   NaN      1      2  23.4500        S   Third  woman      False  NaN  Southampton    no  False
        889         1       1    male  26.0      0      0  30.0000        C   First    man       True    C    Cherbourg   yes   True
        890         0       3    male  32.0      0      0   7.7500        Q   Third    man       True  NaN   Queenstown    no   True

        We want to visualize the counts of different *deck*.

        >>> fig = bs.count_plot(data=data, x="deck")
        >>> plt.show()

    '''

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
    '''
    Draw a strip plot to show the difference between groups in a categorical variable.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and one categorical column.
    x : :py:class:`str`
        The categorical variable to be plotted in x-axis.
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
    swarm_plot : Draw a swarm plot to show the difference between groups in a categorical variable.
    box_plot : Draw a box plot to show the difference between groups in a categorical variable.

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

        We want to visualize the difference of *total_bill* between groups in *day*.

        >>> fig = bs.strip_plot(data=data, x="day", y="total_bill")
        >>> plt.show()

    '''
    
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
    '''
    Draw a swarm plot to show the difference between groups in a categorical variable.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and one categorical column.
    x : :py:class:`str`
        The categorical variable to be plotted in x-axis.
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
    strip_plot : Draw a strip plot to show the difference between groups in a categorical variable.
    box_plot : Draw a box plot to show the difference between groups in a categorical variable.

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

        We want to visualize the difference of *total_bill* between groups in *day*.

        >>> fig = bs.swarm_plot(data=data, x="day", y="total_bill")
        >>> plt.show()

    '''

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
    '''
    Draw a box plot to show the difference between groups in a categorical variable.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and one categorical column.
    x : :py:class:`str`
        The categorical variable to be plotted in x-axis.
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
    boxen_plot : Draw an enhanced box plot to show the difference between groups in a categorical variable.
    strip_plot : Draw a strip plot to show the difference between groups in a categorical variable.

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

        We want to visualize the difference of *total_bill* between groups in *day*.

        >>> fig = bs.box_plot(data=data, x="day", y="total_bill")
        >>> plt.show()

    '''

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
    '''
    Draw an enhanced box plot to show the difference between groups in a categorical variable.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and one categorical column.
    x : :py:class:`str`
        The categorical variable to be plotted in x-axis.
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
    box_plot : Draw a box plot to show the difference between groups in a categorical variable.
    strip_plot : Draw a strip plot to show the difference between groups in a categorical variable.

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

        We want to visualize the difference of *total_bill* between groups in *day*.

        >>> fig = bs.boxen_plot(data=data, x="day", y="total_bill")
        >>> plt.show()

    '''

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
    '''
    Draw a violin plot to show the difference between groups in a categorical variable.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and one categorical column.
    x : :py:class:`str`
        The categorical variable to be plotted in x-axis.
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
    strip_plot : Draw a strip plot to show the difference between groups in a categorical variable.
    box_plot : Draw a box plot to show the difference between groups in a categorical variable.

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

        We want to visualize the difference of *total_bill* between groups in *day*.

        >>> fig = bs.violin_plot(data=data, x="day", y="total_bill")
        >>> plt.show()

    '''

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
    '''
    Draw a bar plot to show the difference between groups in a categorical variable.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column and one categorical column.
    x : :py:class:`str`
        The categorical variable to be plotted in x-axis.
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
    strip_plot : Draw a strip plot to show the difference between groups in a categorical variable.
    box_plot : Draw a box plot to show the difference between groups in a categorical variable.

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

        We want to visualize the difference of *total_bill* between groups in *day*.

        >>> fig = bs.bar_plot(data=data, x="day", y="total_bill")
        >>> plt.show()

    '''

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