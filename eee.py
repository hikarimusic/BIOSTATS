import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt


# t-Test

# One-Sample t-Test
data = pd.read_csv("biostats/dataset/one_sample_t_test.csv")
summary, result = bs.one_sample_t_test(data=data, variable="Angle", expect=120, kind="two-side")
print(summary)
print(result)