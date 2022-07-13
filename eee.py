import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt


# LDA Plot
data = pd.read_csv("biostats/dataset/iris.csv")
fig = bs.lda_plot(data=data, x=["sepal_length", "sepal_width", "petal_length" ,"petal_width"], y="species")
plt.show()

print(data)