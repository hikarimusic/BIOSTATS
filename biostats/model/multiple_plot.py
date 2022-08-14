import matplotlib.pyplot as plt
import seaborn as sns

from biostats.model.util import _CC, _process, _add_p

def ultimate_plot(data, variable):
    '''
    Draw a multiple plot to show the relations between every two variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one column.
    variable : :py:class:`list`
        The list of variables to be plotted.

    Returns
    -------
    fig : :py:class:`matplotlib.figure.Figure`
        The generated plot.

    See also
    --------
    pair_plot : Draw a multiple plot to show the relations between every two numeric variables.
    joint_plot : Draw a combined plot to show the relation between two numeric variables.

    Notes
    -----
    The kinds of plots that will be generated in each grid:
    
    +-------------+-------------+-----------------------+---+
    | Variable 1  | Variable 2  | Plot                  |   |
    +=============+=============+=======================+===+
    | numeric     | -           | histogram             |   |
    +-------------+-------------+-----------------------+---+
    | categorical | -           | count plot            |   |
    +-------------+-------------+-----------------------+---+
    | numeric     | numeric     | scatter plot          |   |
    +-------------+-------------+-----------------------+---+
    | numeric     | categorical | strip plot            |   |
    +-------------+-------------+-----------------------+---+
    | categorical | categorical | count plot (colored)  |   |
    +-------------+-------------+-----------------------+---+

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

        We want to visualize the relations between these variables.

        >>> fig = bs.ultimate_plot(data=data, variable=["species", "bill_length_mm", "body_mass_g", "sex"])
        >>> plt.show()

    '''

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data)

    n = len(variable)
    kind = {}

    for var in variable:
        if str(data.dtypes[var]) == "float64":
            kind[var] = 0
        elif str(data.dtypes[var]) == "Int64":
            if data[var].nunique() > 10:
                data[var] = data[var].astype('float64')
                kind[var] = 0
            else:
                data[var] = data[var].astype('object')
                kind[var] = 1
        else:
            kind[var] = 1
    
    if n == 1:
        fig, ax = plt.subplots()
        axs = {}
        axs[0,0] = ax
    else:
        fig, axs = plt.subplots(n,n, figsize=(8,8))

    for i in range(n):
        for j in range(n):
            if i == j:
                if kind[variable[i]] == 0:
                    sns.histplot(data=data, x=variable[i], ax=axs[i,j])
                else:
                    sns.countplot(data=data, x=variable[i], ax=axs[i,j])
            else:
                if kind[variable[i]] == 0:
                    if kind[variable[j]] == 0:
                        sns.scatterplot(data=data, x=variable[j], y=variable[i], ax=axs[i,j])
                    if kind[variable[j]] == 1:
                        sns.stripplot(data=data, x=variable[j], y=variable[i], ax=axs[i,j])
                if kind[variable[i]] == 1:
                    if kind[variable[j]] == 0:
                        sns.stripplot(data=data, x=variable[j], y=variable[i], ax=axs[i,j])
                    if kind[variable[j]] == 1:
                        sns.countplot(data=data, x=variable[j], hue=variable[i], ax=axs[i,j])
                        axs[i,j].set_ylabel(variable[i])
                        axs[i,j].get_legend().remove()

            if i == n-1:
                axs[i,j].set_xlabel(variable[j])
            else:
                axs[i,j].set_xlabel("")
            if j == 0:
                axs[i,j].set_ylabel(variable[i])
            else:
                axs[i,j].set_ylabel("")
            axs[i,j].set_xticklabels([])
            axs[i,j].set_yticklabels([])

    fig.subplots_adjust(wspace=0.02, hspace=0.02)

    return fig


def pair_plot(data, variable, color=None, kind="scatter"):
    '''
    Draw a multiple plot to show the relations between every two numeric variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least one numeric column.
    variable : :py:class:`list`
        The list of variables to be plotted.
    color : :py:class:`str`
        The categorical variable specifying groups to be plotted with different colors. Maximum 20 groups. Optional. 
    kind : :py:class:`str`
        * "scatter" : Draw scatter plots.
        * "regression" : Draw regression plots.
        * "density" : Draw density plots.
        * "histogram" : Draw histograms.

    Returns
    -------
    fig : :py:class:`matplotlib.figure.Figure`
        The generated plot.

    See also
    --------
    ultimate_plot : Draw a multiple plot to show the relations between every two variables.
    joint_plot : Draw a combined plot to show the relation between two numeric variables.

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

        We want to visualize the relations between these variables.

        >>> fig = bs.pair_plot(data=data, variable=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"], color="species", kind="scatter")
        >>> plt.show()

    '''

    sns.set_theme()
    data = data.dropna(how='all')
    _process(data, num=variable, cat=[color])

    for var in variable:
        if str(data[var].dtypes) not in ("float64", "Int64"):
            raise Warning("The column '{}' must be numeric".format(var))
    if color:
        if data[color].nunique() > 20:
            raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(color))

    if kind == "scatter":
        g = sns.pairplot(data=data, vars=variable, hue=color)
    elif kind == "regression":
        g = sns.pairplot(data=data, vars=variable, hue=color, kind="reg")
    elif kind == "density":
        g = sns.pairplot(data=data, vars=variable, hue=color, kind="kde")
    elif kind == "histogram":
        g = sns.pairplot(data=data, vars=variable, hue=color, kind="hist")
        
    return g.fig

def joint_plot(data, x, y, color=None, kind="scatter"):
    '''
    Draw a combined plot to show the relation between two numeric variables.

    Parameters
    ----------
    data : :py:class:`pandas.DataFrame`
        The input data. Must contain at least two numeric columns. 
    x : :py:class:`str`
        The numeric variable to be plotted in x-axis.
    y : :py:class:`str`
        The numeric variable to be plotted in y-axis.
    color : :py:class:`str`
        The categorical variable specifying groups to be plotted with different colors. Maximum 20 groups. Optional.
    kind : :py:class:`str`
        * "scatter" : Draw scatter plots.
        * "regression" : Draw regression plots.
        * "density" : Draw density plots.
        * "histogram" : Draw histograms.
        * "hexagon" : Draw hexagon plots.

    Returns
    -------
    fig : :py:class:`matplotlib.figure.Figure`
        The generated plot.

    See also
    --------
    ultimate_plot : Draw a multiple plot to show the relations between every two variables.
    pair_plot : Draw a multiple plot to show the relations between every two numeric variables.

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

        We want to visualize the relation between *bill_length_mm* and *bill_depth_mm*.

        >>> fig = bs.joint_plot(data=data, x="bill_length_mm", y="bill_depth_mm", color="species", kind="scatter")
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
            
    if kind == "scatter":
        g = sns.jointplot(data=data, x=x, y=y, hue=color)
    elif kind == "regression":
        g = sns.jointplot(data=data, x=x, y=y, kind="reg")
    elif kind == "density":
        g = sns.jointplot(data=data, x=x, y=y, hue=color, kind="kde")
    elif kind == "histogram":
        g = sns.jointplot(data=data, x=x, y=y, hue=color, kind="hist")
    elif kind == "hexagon":
        g = sns.jointplot(data=data, x=x, y=y, kind="hex")
        
    return g.fig