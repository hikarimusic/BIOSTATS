import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt


# Multivariate ANOVA
data = pd.read_csv("biostats/dataset/multivariate_anova.csv")
summary, result = bs.multivariate_anova(data=data, variable=["sepal_length", "sepal_width"], between="species")
print(summary)
print(result)


