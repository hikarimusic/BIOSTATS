import biostats as bs

def test_anova():
    data = bs.dataset("one_way_anova.csv")
    bs.one_way_anova(data=data, variable="Length", between="Location")

def test_two_way_anova():
    data = bs.dataset("two_way_anova.csv")
    bs.two_way_anova(data=data, variable="Activity", between_1="Sex", between_2="Genotype")

def test_one_way_ancova():
    data = bs.dataset("one_way_ancova.csv")
    summary, result = bs.one_way_ancova(data=data, variable="Pulse", between="Species", covariable="Temp")

def test_two_way_ancova():
    data = bs.dataset("two_way_ancova.csv")
    summary, result = bs.two_way_ancova(data=data, variable="Activity", between_1="Sex", between_2="Genotype", covariable="Age")

def test_multivariate_anova():
    data = bs.dataset("multivariate_anova.csv")
    summary, result = bs.multivariate_anova(data=data, variable=["sepal_length", "sepal_width"], between="species")

def test_repeated_measures_anova():
    data = bs.dataset("repeated_measures_anova.csv")
    summary, result = bs.repeated_measures_anova(data=data, variable="response", between="drug", subject="patient")
