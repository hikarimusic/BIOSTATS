import biostats as bs

def test_count_plot():
    data = bs.dataset("titanic.csv")
    fig = bs.count_plot(data=data, x="deck")

def test_strip_plot():
    data = bs.dataset("tips.csv")
    fig = bs.strip_plot(data=data, x="day", y="total_bill")

def test_swarm_plot():
    data = bs.dataset("tips.csv")
    fig = bs.swarm_plot(data=data, x="day", y="total_bill")

def test_box_plot():
    data = bs.dataset("tips.csv")
    fig = bs.box_plot(data=data, x="day", y="total_bill")

def test_boxen_plot():
    data = bs.dataset("tips.csv")
    fig = bs.boxen_plot(data=data, x="day", y="total_bill")

def test_violin_plot():
    data = bs.dataset("tips.csv")
    fig = bs.violin_plot(data=data, x="day", y="total_bill")

def test_bar_plot():
    data = bs.dataset("tips.csv")
    fig = bs.bar_plot(data=data, x="day", y="total_bill")
