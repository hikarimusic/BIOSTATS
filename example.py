import biostats as bs
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# Basic

# Numeral
data = pd.read_csv("biostats/dataset/numeral.csv")
result = bs.numeral(data=data, variable=["Fish", "Crab", "Temperature"])
print(result)

# Numeral (Grouped)
data = pd.read_csv("biostats/dataset/numeral_grouped.csv")
result = bs.numeral_grouped(data=data, variable="Count", group="Animal")
print(result)

# Categorical
data = pd.read_csv("biostats/dataset/categorical.csv")
result = bs.categorical(data=data, variable="Color")
print(result)

# Contingency
data = pd.read_csv("biostats/dataset/contingency.csv")
result = bs.contingency(data=data, variable_1="Genotype", variable_2="Health", kind="Count")
print(result)

# ---------------------------------------------------------------
# t-Test

# One-Sample t-Test
data = pd.read_csv("biostats/dataset/one_sample_t_test.csv")
summary, result = bs.one_sample_t_test(data=data, variable="Angle", expect=120, kind="two-side")
print(summary)
print(result)

# Two-Sample t-Test
data = pd.read_csv("biostats/dataset/two_sample_t_test.csv")
summary, result = bs.two_sample_t_test(data=data, variable="Value", between="Time", group=["2pm", "5pm"], kind="equal variances")
print(summary)
print(result)

# Paired t-Test
data = pd.read_csv("biostats/dataset/paired_t_test.csv")
summary, result = bs.paired_t_test(data=data, variable="Length", between="Feather", group=["Typical", "Odd"], pair="Bird")
print(summary)
print(result)

# Pairwise t-Test
data = pd.read_csv("biostats/dataset/pairwise_t_test.csv")
summary, result = bs.pairwise_t_test(data=data, variable="Length", between="Location")
print(summary)
print(result)

# ---------------------------------------------------------------
# ANOVA

# One-Way ANOVA
data = pd.read_csv("biostats/dataset/one_way_anova.csv")
summary, result = bs.one_way_anova(data=data, variable="Length", between="Location")
print(summary)
print(result)

# Two-Way ANOVA
data = pd.read_csv("biostats/dataset/two_way_anova.csv")
summary, result = bs.two_way_anova(data=data, variable="Activity", between_1="Sex", between_2="Genotype")
print(summary)
print(result)

# One-Way ANCOVA
data = pd.read_csv("biostats/dataset/one_way_ancova.csv")
summary, result = bs.one_way_ancova(data=data, variable="Pulse", between="Species", covariable="Temp")
print(summary)
print(result)

# Two-Way ANCOVA
data = pd.read_csv("biostats/dataset/two_way_ancova.csv")
summary, result = bs.two_way_ancova(data=data, variable="Activity", between_1="Sex", between_2="Genotype", covariable="Age")
print(summary)
print(result)

# Multivariate ANOVA
data = pd.read_csv("biostats/dataset/multivariate_anova.csv")
summary, result = bs.multivariate_anova(data=data, variable=["sepal_length", "sepal_width"], between="species")
print(summary)
print(result)

# Repeated Measures ANOVA
data = pd.read_csv("biostats/dataset/repeated_measures_anova.csv")
summary, result = bs.repeated_measures_anova(data=data, variable="response", between="drug", subject="patient")
print(summary)
print(result)

# ---------------------------------------------------------------
# Exact Test

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

# McNemar's Exact Test
data = pd.read_csv("biostats/dataset/mcnemar_exact_test.csv")
summary, result = bs.mcnemar_exact_test(data=data, variable_1="Treatment", variable_2="Result", pair="ID")
print(summary)
print(result)

# ---------------------------------------------------------------
# Chi-Square Test

# Chi-Square Test
data = pd.read_csv("biostats/dataset/chi_square_test.csv")
summary, result = bs.chi_square_test(data=data, variable_1="Genotype", variable_2="Health")
print(summary)
print(result)

# Chi-Square Test (Fit)
data = pd.read_csv("biostats/dataset/chi_square_test_fit.csv")
summary, result = bs.chi_square_test_fit(data=data, variable="Canopy", expect={"Douglas":0.54, "Ponderosa":0.40, "Grand":0.05, "Western":0.01})
print(summary)
print(result)

# McNemar's Test
data = pd.read_csv("biostats/dataset/mcnemar_test.csv")
summary, result = bs.mcnemar_test(data=data, variable_1="Treatment", variable_2="Result", pair="ID")
print(summary)
print(result)

# Mantel-Haenszel Test
data = pd.read_csv("biostats/dataset/mantel_haenszel_test.csv")
summary, result = bs.mantel_haenszel_test(data=data, variable_1="Treatment", variable_2="Revascularization", stratum="Study")
print(summary)
print(result)

# ---------------------------------------------------------------
# Linear Regression

# Correlation
data = pd.read_csv("biostats/dataset/correlation.csv")
summary, result = bs.correlation(data=data, x="Latitude", y="Species")
print(summary)
print(result)

# Correlation Matrix
data = pd.read_csv("biostats/dataset/correlation_matrix.csv")
summary = bs.correlation_matrix(data=data, variable=["Stream","Longnose","Acerage","DO2","Maxdepth","NO3","SO4","Temp"])
print(summary)

# Simple Linear Regression
data = pd.read_csv("biostats/dataset/simple_linear_regression.csv")
summary, result = bs.simple_linear_regression(data=data, x="Weight", y="Eggs")
print(summary)
print(result)

# Multiple Linear Regression
data = pd.read_csv("biostats/dataset/multiple_linear_regression.csv")
summary, result = bs.multiple_linear_regression(data=data, x_nominal=["Acerage", "Maxdepth", "NO3"], x_categorical=[], y="Longnose")
print(summary)
print(result)

# ---------------------------------------------------------------
# Logistic Regression

# Simple Logistic Regression
data = pd.read_csv("biostats/dataset/simple_logistic_regression.csv")
summary, result = bs.simple_logistic_regression(data=data, x="Continuous", y="Factor", target="B")
print(summary)
print(result)

# Multiple Logistic Regression
data = pd.read_csv("biostats/dataset/multiple_logistic_regression.csv")
summary, result = bs.multiple_logistic_regression(data=data, x_nominal=["Upland", "Migr", "Mass", "Indiv", "Insect", "Wood"], x_categorical=[], y="Status", target=1)
print(summary)
print(result)

# Ordered Logistic Regression
data = pd.read_csv("biostats/dataset/ordered_logistic_regression.csv")
summary, result = bs.ordered_logistic_regression(data=data, x_nominal=["pared", "public", "gpa"], x_categorical=[], y="apply", 
    order={"unlikely":1, "somewhat likely":2, "very likely":3})
print(summary)
print(result)

# Multinomial Logistic Regression
data = pd.read_csv("biostats/dataset/multinomial_logistic_regression.csv")
summary, result = bs.multinomial_logistic_regression(data=data, x_nominal=["write"], x_categorical=["ses"], y="prog", baseline="academic")
print(summary)
print(result)

# ---------------------------------------------------------------
# Nonparametric

# Median Test
data = pd.read_csv("biostats/dataset/median_test.csv")
summary, result = bs.median_test(data=data, variable="Value", expect=3)
print(summary)
print(result)

# Sign Test
data = pd.read_csv("biostats/dataset/sign_test.csv")
summary, result = bs.sign_test(data=data, variable="Concentration", between="Month", group=["August", "November"], pair="Clone")
print(summary)
print(result)

# Wilcoxon Signed-Rank Test
data = pd.read_csv("biostats/dataset/wilcoxon_signed_rank_test.csv")
summary, result = bs.wilcoxon_signed_rank_test(data=data, variable="Concentration", between="Month", group=["August", "November"], pair="Clone")
print(summary)
print(result)

# Wilcoxon Rank-Sum Test
data = pd.read_csv("biostats/dataset/two_sample_t_test.csv")
summary, result = bs.wilcoxon_rank_sum_test(data=data, variable="Value", between="Time", group=["2pm", "5pm"])
print(summary)
print(result)

# Kruskal-Wallis Test
data = pd.read_csv("biostats/dataset/kruskal_wallis_test.csv")
summary, result = bs.kruskal_wallis_test(data=data, variable="Value", between="Group")
print(summary)
print(result)

# Friedman Test
data = pd.read_csv("biostats/dataset/friedman_test.csv")
summary, result = bs.friedman_test(data=data, variable="response", between="drug", subject="patient")
print(summary)
print(result)

# Spearman's Rank Correlation
data = pd.read_csv("biostats/dataset/spearman_rank_correlation.csv")
summary, result = bs.spearman_rank_correlation(data=data, x="Volume", y="Pitch")
print(summary)
print(result)

# ---------------------------------------------------------------
# Others

# Linear Discriminant Analysis
data = pd.read_csv("biostats/dataset/linear_discriminant_analysis.csv")
summary, result, prediction = bs.linear_discriminant_analysis(data=data, x=["sepal_length", "sepal_width", "petal_length" ,"petal_width"], y="species", 
    predict={"sepal_length": 5.7, "sepal_width": 2.7, "petal_length": 4.0 ,"petal_width":1.4})
print(summary)
print(result)
print(prediction)

# Principal Component Analysis
data = pd.read_csv("biostats/dataset/principal_component_analysis.csv")
summary, result, transformation = bs.principal_component_analysis(data=data, x=["Murder", "Assault", "UrbanPop", "Rape"], 
    transform={"Murder":10.2, "Assault":211, "UrbanPop":67, "Rape":32.3})
print(summary)
print(result)
print(transformation)

# ---------------------------------------------------------------
# Distribution

# Histogram
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.histogram(data=data, x="flipper_length_mm", band=10, color="species")
plt.show()

# Density Plot
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.density_plot(data=data, x="flipper_length_mm", smooth=1, color="species")
plt.show()

# Cumulative Plot
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.cumulative_plot(data=data, x="bill_length_mm", color="species")
plt.show()

# 2D Histogram
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.histogram_2D(data=data, x="bill_depth_mm", y="body_mass_g", color="species")
plt.show()

# 2D Density Plot
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.density_plot_2D(data=data, x="bill_depth_mm", y="body_mass_g", color="species")
plt.show()

# ---------------------------------------------------------------
# Categorical

# Count Plot
data = pd.read_csv("biostats/dataset/titanic.csv")
fig = bs.count_plot(data=data, x="class", color="who")
plt.show()

# Strip Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.strip_plot(data=data, x="day", y="total_bill", color="smoker")
plt.show()

# Strip Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.swarm_plot(data=data, x="day", y="total_bill", color="smoker")
plt.show()

# Box Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.box_plot(data=data, x="day", y="total_bill", color="smoker")
plt.show()

# Boxen Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.boxen_plot(data=data, x="day", y="total_bill", color="smoker")
plt.show()

# Violin Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.violin_plot(data=data, x="day", y="total_bill", color="smoker")
plt.show()

# Bar Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.bar_plot(data=data, x="day", y="total_bill", color="smoker")
plt.show()

# ---------------------------------------------------------------
# Relational

# Scatter Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.scatter_plot(data=data, x="total_bill", y="tip", color="time")
plt.show()

# Line Plot
data = pd.read_csv("biostats/dataset/flights.csv")
fig = bs.line_plot(data=data, x="year", y="passengers", color="month")
plt.show()

# Regression Plot
data = pd.read_csv("biostats/dataset/tips.csv")
fig = bs.regression_plot(data=data, x="total_bill", y="tip")
plt.show()

# ---------------------------------------------------------------
# Multiple

# Ultimate Plot
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.ultimate_plot(data=data, variable=["species", "bill_length_mm", "body_mass_g", "sex"])
plt.show()

# Pair Plot
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.pair_plot(data=data, variable=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"], color="species", kind="scatter")
plt.show()

# Joint Plot
data = pd.read_csv("biostats/dataset/penguins.csv")
fig = bs.joint_plot(data=data, x="bill_length_mm", y="bill_depth_mm", color="species", kind="scatter")
plt.show()

# ---------------------------------------------------------------
# Others

# PCA Plot
data = pd.read_csv("biostats/dataset/iris.csv")
fig = bs.pca_plot(data=data, x=["sepal_length", "sepal_width", "petal_length" ,"petal_width"], color="species")
plt.show()

# LDA Plot
data = pd.read_csv("biostats/dataset/iris.csv")
fig = bs.lda_plot(data=data, x=["sepal_length", "sepal_width", "petal_length" ,"petal_width"], y="species")
plt.show()