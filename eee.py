import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt

# Binomial Test
data = pd.read_csv("biostats/dataset/binomial_test.csv")
summary, result = bs.binomial_test(data=data, variable="Flower", expect={"Purple":9, "Red":3, "Blue":3, "White":1})
print(summary)
print(result)

# Fisher's Exact Test
data = pd.read_csv("biostats/dataset/fisher_exact_test.csv")
summary, result = bs.fisher_exact_test(data=data, variable_1="Frequency", variable_2="Result")
print(summary)
print(result)