import numpy as np
import pandas as pd



'''
from anova import one_way_anova
data = pd.read_csv("anova.csv")
print(one_way_anova(data, "Pain threshold", "Hair color"))
'''

'''
from anova import two_way_anova
data = pd.read_csv("anova2.csv")
print(two_way_anova(data, "Yield", ["Blend", "Crop"]))
'''

'''
from anova import N_way_anova
data = pd.read_csv("anova3.csv")
print(N_way_anova(data, "Cholesterol", ['Sex', 'Risk', 'Drug'],1))
'''


from regression import linear_regression
data = pd.read_csv("regression.csv")
print(linear_regression(data, "tip", "total_bill", 1))

'''
from regression import multiple_regression
data = pd.read_csv("regression.csv")
print(multiple_regression(data, "tip", ["total_bill", "size"], 1))
'''
