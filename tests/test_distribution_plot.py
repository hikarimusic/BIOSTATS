import biostats as bs

def test_histogram():
    data = bs.dataset("penguins.csv")
    fig = bs.histogram(data=data, x="flipper_length_mm", band=10, color="species")

def test_density_plot():
    data = bs.dataset("penguins.csv")
    fig = bs.density_plot(data=data, x="flipper_length_mm", smooth=1, color="species")

def test_cumulative_plot():
    data = bs.dataset("penguins.csv")
    fig = bs.density_plot(data=data, x="flipper_length_mm", smooth=1, color="species")

def test_histogram_2D():
    data = bs.dataset("penguins.csv")
    fig = bs.histogram_2D(data=data, x="bill_depth_mm", y="body_mass_g", color="species")

def test_density_plot_2D():
    data = bs.dataset("penguins.csv")
    fig = bs.density_plot_2D(data=data, x="bill_depth_mm", y="body_mass_g", color="species")