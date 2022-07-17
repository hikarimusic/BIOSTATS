import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt

"""
# Principal Component Analysis
data = pd.read_csv("biostats/dataset/principal_component_analysis.csv")
summary, result, transformation = bs.principal_component_analysis(data=data, x=["Murder", "Assault", "UrbanPop", "Rape"], 
    transform={"Murder":10.2, "Assault":211, "UrbanPop":67, "Rape":32.3})
print(summary)
print(result)
print(transformation)

"""

# LDA Plot
data = pd.read_csv("biostats/dataset/iris.csv")
fig = bs.pca_plot(data=data, x=["sepal_length", "sepal_width", "petal_length" ,"petal_width"], color="species")
plt.show()