import biostats as bs

def test_scatter_plot():
    data = bs.dataset("tips.csv")
    fig = bs.scatter_plot(data=data, x="total_bill", y="tip", color="day")

def test_line_plot():
    data = bs.dataset("flights.csv")
    fig = bs.line_plot(data=data, x="year", y="passengers", color="month")

def test_regression_plot():
    data = bs.dataset("tips.csv")
    fig = bs.regression_plot(data=data, x="total_bill", y="tip")