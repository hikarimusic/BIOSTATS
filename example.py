import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# Basic

# Numeral
data = pd.read_csv("biostats/dataset/numeral.csv")
result = bs.numeral(data=data, variable=["Fish", "Crab", "Temperature"])
print(result)

# ---------------------------------------------------------------
# t-Test

# One-Sample t-Test
data = pd.read_csv("biostats/dataset/one_sample_t_test.csv")
summary, result = bs.one_sample_t_test(data=data, variable="Angle", expect=120, kind="two-side")
print(summary)
print(result)

# ---------------------------------------------------------------
# ANOVA

# One-Way ANOVA
data = pd.read_csv("biostats/dataset/one_way_anova.csv")
summary, result = bs.one_way_anova(data=data, variable="Length", between="Location")
print(summary)
print(result)

# ---------------------------------------------------------------
# Distribution

# Histogram
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.histogram(data=data, x="flipper_length_mm", band=10, color="species")
plt.show()

# Density Plot
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.density(data=data, x="flipper_length_mm", smooth=1, color="species")
plt.show()