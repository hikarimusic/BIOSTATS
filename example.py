from numpy import var
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
fig = bs.density_plot(data=data, x="flipper_length_mm", smooth=1, color="species")
plt.show()

# Cumulative Plot
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.cumulative_plot(data=data, x="bill_length_mm", color="species")
plt.show()

# 2D Histogram
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.histogram_2D(data=data, x="bill_depth_mm", y="body_mass_g", color="species")
plt.show()

# 2D Density Plot
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.density_plot_2D(data=data, x="bill_depth_mm", y="body_mass_g", color="species")
plt.show()

# ---------------------------------------------------------------
# Categorical

# Count Plot
data = pd.read_csv("biostats/dataset/titanic.csv")
fig = bs.count_plot(data=data, x="class", color="who")
plt.show()

# Strip Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.strip_plot(data=data, x="day", y="total_bill", color="smoker")
plt.show()

# Strip Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.swarm_plot(data=data, x="day", y="total_bill", color="smoker")
plt.show()

# Box Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.box_plot(data=data, x="day", y="total_bill", color="smoker")
plt.show()

# Boxen Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.boxen_plot(data=data, x="day", y="total_bill", color="smoker")
plt.show()

# Violin Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.violin_plot(data=data, x="day", y="total_bill", color="smoker")
plt.show()

# Bar Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.bar_plot(data=data, x="day", y="total_bill", color="smoker")
plt.show()

# ---------------------------------------------------------------
# Relational

# Scatter Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.scatter_plot(data=data, x="total_bill", y="tip", color="time")
plt.show()

# Line Plot
data = pd.read_csv("biostats/dataset/flights.csv")
fig = bs.line_plot(data=data, x="year", y="passengers", color="month")
plt.show()

# Regression Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.regression_plot(data=data, x="total_bill", y="tip")
plt.show()

# ---------------------------------------------------------------
# Multiple

# Ultimate Plot
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.ultimate_plot(data=data, variable=["species", "bill_length_mm", "body_mass_g", "sex"])
plt.show()

# Pair Plot
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.pair_plot(data=data, variable=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"], color="species", kind="scatter")
plt.show()

# Joint Plot
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.joint_plot(data=data, x="bill_length_mm", y="bill_depth_mm", color="species", kind="scatter")
plt.show()