import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt


# Contingency
data = pd.read_csv("biostats/dataset/contingency.csv")
result = bs.contingency(data=data, variable_1="Genotype", variable_2="Health", kind="Count")
print(result)