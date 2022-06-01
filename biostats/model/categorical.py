import matplotlib.pyplot as plt
import seaborn as sns

def process(data):
    for col in data:
        try: 
            data[col] = data[col].astype('float64')
        except:
            pass  

def strip(data, x, y, color=None):

    sns.set_theme()
    process(data)

    fig, ax = plt.subplots()
    if color:
        sns.stripplot(data=data, x=x, y=y, hue=color, ax=ax)
    else:
        sns.stripplot(data=data, x=x, y=y, ax=ax)
        
    return fig
