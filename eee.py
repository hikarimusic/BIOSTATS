import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt


# Strip Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.strip(data=data, x="day", y="total_bill", color="smoker")
plt.show()