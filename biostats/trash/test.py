import numpy as np
import pandas as pd

'' '
from anova import one_way_anova
data = pd.read_csv("data_anova.csv")
print(one_way_anova(data, "Pain threshold", "Hair color", 1))
'' '

'' '
from anova import two_way_anova
data = pd.read_csv("data_anova2.csv")
print(two_way_anova(data, "Yield", ["Blend", "Crop"], 1))
'' '

'' '
from anova import N_way_anova
data = pd.read_csv("data_anova3.csv")
print(N_way_anova(data, "Cholesterol", ['Sex', 'Risk', 'Drug'], 1))
'' '

'' '
from regression import linear_regression
data = pd.read_csv("data_regression.csv")
print(linear_regression(data, "tip", "total_bill", 1))
'' '

'' '
from regression import multiple_regression
data = pd.read_csv("data_regression.csv")
print(multiple_regression(data, "tip", ["total_bill", "size"], 1))
'' '

'' '
from regression import logistic_regression
data = pd.read_csv("data_logistic.csv")
print(logistic_regression(data, "sex", ["body_mass_g"], "male"))
'' '

'' '
from ancova import one_way_ancova
data = pd.read_csv("data_ancova.csv")
print(one_way_ancova(data, "Scores", "Method", "Income", 1))
'' '

'' '
from ancova import two_way_ancova
data = pd.read_csv("data_ancova.csv")
print(two_way_ancova(data, "Scores", "Method", ["Income", "BMI"], 1))
'' '

'' '
from ancova import N_way_ancova
data = pd.read_csv("data_ancova.csv")
print(N_way_ancova(data, "Scores", "Method", ["Income", "BMI"], 1))
'' '

from chi_square import chi_square_test
data = pd.read_csv("data_chi2.csv")
print(chi_square_test(data, "sex", "target", 1))