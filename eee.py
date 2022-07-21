import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt

# Heatmap
data = bs.dataset("flights.csv")
fig = bs.heatmap(data=data, x="year", y="month", value="passengers")
plt.show()