import matplotlib.pyplot as plt
import seaborn as sns

def process(data):
    for col in data:
        try: 
            data[col] = data[col].astype('float64')
        except:
            pass  

def histogram(data, x, band, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    if color:
        sns.histplot(data=data, x=x, bins=band, hue=color, ax=ax)
    else:
        sns.histplot(data=data, x=x, bins=band, ax=ax)
        
    return fig


def density(data, x, smooth, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    if color:
        sns.kdeplot(data= data, x=x, bw_adjust=smooth, hue=color, ax=ax)
    else:
        sns.kdeplot(data=data, x=x, bw_adjust=smooth, ax=ax)
    
    return fig
