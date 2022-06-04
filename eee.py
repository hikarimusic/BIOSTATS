import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt

# Ultimate Plot
'''
data = pd.read_csv("biostats/dataset/chi_square_test.csv")
summary, result = bs.chi_square_test(data=data, variable_1="Genotype", variable_2="Health")
print(summary)
print(result)
'''


# Fisher's Exact Test
data = pd.read_csv("biostats/dataset/fisher_exact_test.csv")
summary, result = bs.fisher_exact_test(data=data, variable_1="Frequency", variable_2="Result")
print(summary)
print(result)

'''
# Chi-Square Test
data = pd.read_csv("biostats/dataset/fisher_exact_test.csv")
summary, result = bs.chi_square_test(data=data, variable_1="Frequency", variable_2="Frequency")
print(summary)
print(result)
'''