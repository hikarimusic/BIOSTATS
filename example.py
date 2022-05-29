import biostats as bs
import pandas as pd

# ---------------------------------------------------------------
# Basic

# Numeral
data = pd.read_csv("biostats/dataset/numeral.csv")
result = bs.numeral(data, ["Fish", "Crab", "Temperature"])
#print(result)

# ---------------------------------------------------------------
# ANOVA

# One-Way ANOVA
data = pd.read_csv("biostats/dataset/one_way_anova.csv")
summary, result = bs.one_way_anova(data, "Length", "Location")
print(summary)
print(result)
