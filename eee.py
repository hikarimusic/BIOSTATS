import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt


# Paired t-Test
data = pd.read_csv("biostats/dataset/paired_t_test.csv")
summary, result = bs.paired_t_test(data=data, variable_1="Typical", variable_2="Odd", kind="two-side")
print(summary)
print(result)