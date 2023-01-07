import biostats as bs

def test_ultimate_plot():
    data = bs.dataset("penguins.csv")
    fig = bs.ultimate_plot(data=data, variable=["species", "bill_length_mm", "body_mass_g", "sex"])

def test_pair_plot():
    data = bs.dataset("penguins.csv")
    fig = bs.pair_plot(data=data, variable=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"], color="species", kind="scatter")

def test_joint_plot():
    data = bs.dataset("penguins.csv")
    fig = bs.joint_plot(data=data, x="bill_length_mm", y="bill_depth_mm", color="species", kind="scatter")