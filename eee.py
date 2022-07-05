import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt


# Two-Way ANOVA
data = pd.read_csv("biostats/dataset/two_way_anova.csv")
summary, result = bs.two_way_anova(data=data, variable="Activity", between_1="Sex", between_2="Genotype")
print(summary)
print(result)

