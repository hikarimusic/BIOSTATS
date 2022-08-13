import biostats as bs
import matplotlib.pyplot as plt

# Ultimate Plot
data = bs.dataset("penguins.csv")
fig = bs.ultimate_plot(data=data, variable=["species", "bill_length_mm", "body_mass_g", "sex"])
plt.show()

# Pair Plot
data = bs.dataset("penguins.csv")
fig = bs.pair_plot(data=data, variable=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"], color="species", kind="scatter")
plt.show()

# Joint Plot
data = bs.dataset("penguins.csv")
fig = bs.joint_plot(data=data, x="bill_length_mm", y="bill_depth_mm", color="species", kind="scatter")
plt.show()