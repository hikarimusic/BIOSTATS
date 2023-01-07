import biostats as bs

def test_numeric():
    data = bs.dataset("numeric.csv")
    result = bs.numeric(data=data, variable=["Fish", "Crab", "Temperature"])

def test_numeric_grouped():
    data = bs.dataset("numeric_grouped.csv")
    result = bs.numeric_grouped(data=data, variable="Count", group="Animal")

def test_categorical():
    data = bs.dataset("categorical.csv")
    result = bs.categorical(data=data, variable="Color")

def test_contingency():
    data = bs.dataset("contingency.csv")
    result = bs.contingency(data=data, variable_1="Genotype", variable_2="Health", kind="count")
