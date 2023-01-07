import biostats as bs

def test_simple_logistic_regression():
    data = bs.dataset("simple_logistic_regression.csv")
    summary, result = bs.simple_logistic_regression(data=data, x="Continuous", y="Factor", target="B")

def test_multiple_logistic_regression():
    data = bs.dataset("multiple_logistic_regression.csv")
    summary, result = bs.multiple_logistic_regression(data=data, x_numeric=["Upland", "Migr", "Mass", "Indiv", "Insect", "Wood"], x_categorical=[], y="Status", target=1)

def test_ordered_logistic_regression():
    data = bs.dataset("ordered_logistic_regression.csv")
    summary, result = bs.ordered_logistic_regression(data=data, x_numeric=["pared", "public", "gpa"], x_categorical=[], y="apply", order={"unlikely":1, "somewhat likely":2, "very likely":3})

def test_multinomial_logistic_regression():
    data = bs.dataset("multinomial_logistic_regression.csv")
    summary, result = bs.multinomial_logistic_regression(data=data, x_numeric=["write"], x_categorical=["ses"], y="prog", baseline="academic")