import biostats as bs

def test_chi_square_test():
    data = bs.dataset("chi_square_test.csv")
    summary, result = bs.chi_square_test(data=data, variable_1="Genotype", variable_2="Health", kind="horizontal")

def test_chi_square_test_fit():
    data = bs.dataset("chi_square_test_fit.csv")
    summary, result = bs.chi_square_test_fit(data=data, variable="Canopy", expect={"Douglas":0.54, "Ponderosa":0.40, "Grand":0.05, "Western":0.01})

def test_mcnemar_test():
    data = bs.dataset("mcnemar_test.csv")
    summary, result = bs.mcnemar_test(data=data, variable_1="Treatment", variable_2="Result", pair="ID")

def test_mantel_haenszel_test():
    data = bs.dataset("mantel_haenszel_test.csv")
    summary, result = bs.mantel_haenszel_test(data=data, variable_1="Treatment", variable_2="Revascularization", stratum="Study")
