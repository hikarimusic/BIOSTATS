import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt


# FA Plot
data = pd.read_csv("biostats/dataset/iris.csv")
fig = bs.fa_plot(data=data, x=["sepal_length", "sepal_width", "petal_length" ,"petal_width"], factors=2, color="species")
plt.show()