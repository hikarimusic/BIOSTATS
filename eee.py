import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt

# 2D Density Plot
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.density_plot_2D(data=data, x="bill_depth_mm", y="body_mass_g", color="species")
plt.show()