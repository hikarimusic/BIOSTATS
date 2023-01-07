import biostats as bs

def test_binomial_test():
    data = bs.dataset("binomial_test.csv")
    summary, result = bs.binomial_test(data=data, variable="Flower", expect={"Purple":9, "Red":3, "Blue":3, "White":1})

def test_fisher_exact_test():
    data = bs.dataset("fisher_exact_test.csv")
    summary, result = bs.fisher_exact_test(data=data, variable_1="Frequency", variable_2="Result", kind="horizontal")

def test_mcnemar_exact_test():
    data = bs.dataset("mcnemar_exact_test.csv")
    summary, result = bs.mcnemar_exact_test(data=data, variable_1="Treatment", variable_2="Result", pair="ID")