import biostats as bs

def test_correlation():
    data = bs.dataset("correlation.csv")
    summary, result = bs.correlation(data=data, x="Latitude", y="Species")

def test_correlation_matrix():
    data = bs.dataset("correlation_matrix.csv")
    summary = bs.correlation_matrix(data=data, variable=["Longnose","Acerage","DO2","Maxdepth","NO3","SO4","Temp"])

def test_simple_linear_regression():
    data = bs.dataset("simple_linear_regression.csv")
    summary, result = bs.simple_linear_regression(data=data, x="Weight", y="Eggs")

def test_multiple_linear_regression():
    data = bs.dataset("multiple_linear_regression.csv")
    summary, result = bs.multiple_linear_regression(data=data, x_numeric=["Acerage", "Maxdepth", "NO3"], x_categorical=[], y="Longnose")