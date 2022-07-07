import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt


# Paired t-Test
data = pd.read_csv("biostats/dataset/paired_t_test.csv")
summary, result = bs.paired_t_test(data=data, variable="Length", between="Feather", group=["Typical", "Odd"], pair="Bird")
print(summary)
print(result)