import matplotlib.pyplot as plt
import seaborn as sns

def process(data):
    for col in data:
        try: 
            data[col] = data[col].astype('float64')
        except:
            pass  

def scatter_plot(data, x, y, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    if color:
        sns.scatterplot(data=data, x=x, y=y, hue=color, ax=ax)
    else:
        sns.scatterplot(data=data, x=x, y=y, ax=ax)
        
    return fig

def line_plot(data, x, y, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    if color:
        sns.lineplot(data=data, x=x, y=y, hue=color, ax=ax)
    else:
        sns.lineplot(data=data, x=x, y=y, ax=ax)
        
    return fig

def regression_plot(data, x, y):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    sns.regplot(data=data, x=x, y=y, ax=ax)
        
    return fig