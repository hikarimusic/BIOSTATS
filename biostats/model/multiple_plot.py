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

def ultimate_plot(data, variable):

    sns.set_theme()
    process(data)

    for var in variable:
        if str(data[var].dtypes) != "float64":
            if data[var].nunique() > 20:
                raise Warning("The nmuber of classes in column '{}' cannot > 20.".format(var))

    n = len(variable)
    kind = {}

    for var in variable:
        if str(data.dtypes[var]) == "float64":
            kind[var] = 0
        else:
            kind[var] = 1
    
    if n == 1:
        fig, ax = plt.subplots()
        axs = {}
        axs[0,0] = ax
    else:
        fig, axs = plt.subplots(n,n)

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

"""
fig, axs= plt.subplots(2,2)
sns.stripplot(x="Location", y="Length", data=data, ax=axs[0,0])
sns.swarmplot(x="Location", y="Length", data=data, ax=axs[0,1])
sns.stripplot(x="Location", y="Length", data=data, ax=axs[1,0])
sns.swarmplot(x="Location", y="Length", data=data, ax=axs[1,1])

m = 2
n = 2

for i in range(m):
    for j in range (n):
        if i != m-1:
            axs[i,j].set_xlabel("")
            axs[i,j].set_xticklabels([])
        if j != 0:
            axs[i,j].set_ylabel("")
            axs[i,j].set_yticklabels([])
        plt.sca(axs[i,j])
        plt.xticks(rotation=90)


fig.subplots_adjust(wspace=0.02, hspace=0.02)
"""



def pair_plot(data, variable, color=None, kind="scatter"):

    sns.set_theme()
    process(data)

    for var in variable:
        if str(data[var].dtypes) != "float64":
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

    sns.set_theme()
    process(data)

    if str(data[x].dtypes) != "float64":
        raise Warning("The column '{}' must be numeric".format(x))
    if str(data[y].dtypes) != "float64":
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