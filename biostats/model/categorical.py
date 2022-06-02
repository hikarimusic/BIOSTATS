import matplotlib.pyplot as plt
import seaborn as sns

def process(data):
    for col in data:
        try: 
            data[col] = data[col].astype('float64')
        except:
            pass  

def count_plot(data, x, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    if color:
        sns.countplot(data=data, x=x, hue=color, ax=ax)
    else:
        sns.countplot(data=data, x=x, ax=ax)
        
    return fig

def strip_plot(data, x, y, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    if color:
        sns.stripplot(data=data, x=x, y=y, hue=color, ax=ax)
    else:
        sns.stripplot(data=data, x=x, y=y, ax=ax)
        
    return fig

def swarm_plot(data, x, y, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    if color:
        sns.swarmplot(data=data, x=x, y=y, hue=color, ax=ax)
    else:
        sns.swarmplot(data=data, x=x, y=y, ax=ax)
        
    return fig

def box_plot(data, x, y, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    if color:
        sns.boxplot(data=data, x=x, y=y, hue=color, ax=ax)
    else:
        sns.boxplot(data=data, x=x, y=y, ax=ax)
        
    return fig

def boxen_plot(data, x, y, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    if color:
        sns.boxenplot(data=data, x=x, y=y, hue=color, ax=ax)
    else:
        sns.boxenplot(data=data, x=x, y=y, ax=ax)
        
    return fig

def violin_plot(data, x, y, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    if color:
        sns.violinplot(data=data, x=x, y=y, hue=color, ax=ax)
    else:
        sns.violinplot(data=data, x=x, y=y, ax=ax)
        
    return fig

def bar_plot(data, x, y, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    if color:
        sns.barplot(data=data, x=x, y=y, hue=color, ax=ax)
    else:
        sns.barplot(data=data, x=x, y=y, ax=ax)
        
    return fig