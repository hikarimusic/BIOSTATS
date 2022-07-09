import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt


# Correlation Matrix
data = pd.read_csv("biostats/dataset/correlation_matrix.csv")
summary = bs.correlation_matrix(data=data, variable=["Stream","Longnose","Acerage","DO2","Maxdepth","NO3","SO4","Temp"])
print(summary)
