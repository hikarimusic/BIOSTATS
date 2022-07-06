import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt


# ANCOVA
data = pd.read_csv("biostats/dataset/ancova.csv")
summary, result = bs.ancova(data=data, variable="Pulse", between="Species", covariable="Temp")
print(summary)
print(result)