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

def count_plot(data, x, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    sns.countplot(data=data, x=x, hue=color, ax=ax)
        
    return fig

def strip_plot(data, x, y, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    sns.stripplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig

def swarm_plot(data, x, y, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    sns.swarmplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig

def box_plot(data, x, y, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    sns.boxplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig

def boxen_plot(data, x, y, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    sns.boxenplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig

def violin_plot(data, x, y, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    sns.violinplot(data=data, x=x, y=y, hue=color, ax=ax)

    return fig

def bar_plot(data, x, y, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    sns.barplot(data=data, x=x, y=y, hue=color, ax=ax)
        
    return fig