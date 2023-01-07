import biostats as bs

def test_heatmap():
    data = bs.dataset("flights.csv")
    fig = bs.heatmap(data=data, x="year", y="month", value="passengers")

def test_fa_plot():
    data = bs.dataset("iris.csv")
    fig = bs.fa_plot(data=data, x=["sepal_length", "sepal_width", "petal_length" ,"petal_width"], factors=2, color="species")

def test_pca_plot():
    data = bs.dataset("iris.csv")
    fig = bs.pca_plot(data=data, x=["sepal_length", "sepal_width", "petal_length" ,"petal_width"], color="species")

def test_lda_plot():
    data = bs.dataset("iris.csv")
    fig = bs.lda_plot(data=data, x=["sepal_length", "sepal_width", "petal_length" ,"petal_width"], y="species")