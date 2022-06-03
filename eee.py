import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt

# Ultimate Plot
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.ultimate_plot(data=data, variable=["species", "bill_length_mm", "body_mass_g", "sex"])
plt.show()