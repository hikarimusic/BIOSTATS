import biostats as bs
import pandas as pd

# ---------------------------------------------------------------
#Basic

# Numeral
data = pd.read_csv("biostats/dataset/numeral.csv")
r1, r2, r3, r4 = bs.numeral(data, ["Fish", "Crab", "Temperature"])
print(r1)
print(r2)
print(r3)
print(r4)
