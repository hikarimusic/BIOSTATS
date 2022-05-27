import biostats as bs
import pandas as pd

# ---------------------------------------------------------------
#Basic

# Numeral
data = pd.read_csv("biostats/dataset/numeral.csv")
result = bs.numeral(data, ["Fish", "Crab", "Temperature"])
print(result)

