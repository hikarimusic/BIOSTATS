import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt


# Pairwise t-Test
data = pd.read_csv("biostats/dataset/pairwise_t_test.csv")
summary, result = bs.pairwise_t_test(data=data, variable="Length", between="Location")
print(summary)
print(result)