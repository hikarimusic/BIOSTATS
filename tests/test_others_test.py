import biostats as bs

def test_screening_test():
    data = bs.dataset("screening_test.csv")
    summary, result = bs.screening_test(data=data, disease="Cancer", disease_target="Present", test="PSA Test", test_target="Positive")

def test_epidemiologic_study():
    data = bs.dataset("epidemiologic_study.csv")
    summary, result = bs.epidemiologic_study(data=data, disease="MI", disease_target="Occur", factor="Diabetes", factor_target="Yes")

def test_factor_analysis():
    data = bs.dataset("factor_analysis.csv")
    summary, result, analysis = bs.factor_analysis(data=data, x=["Oil", "Density", "Crispy", "Fracture", "Hardness"], factors=2, analyze={"Oil":17.2, "Density":2830, "Crispy":12, "Fracture":19, "Hardness":121})

def test_principal_component_analysis():
    data = bs.dataset("principal_component_analysis.csv")
    summary, result, transformation = bs.principal_component_analysis(data=data, x=["Murder", "Assault", "UrbanPop", "Rape"], transform={"Murder":10.2, "Assault":211, "UrbanPop":67, "Rape":32.3})

def test_linear_discriminant_analysis():
    data = bs.dataset("linear_discriminant_analysis.csv")
    summary, result, prediction = bs.linear_discriminant_analysis(data=data, x=["sepal_length", "sepal_width", "petal_length" ,"petal_width"], y="species", predict={"sepal_length": 5.7, "sepal_width": 2.7, "petal_length": 4.0 ,"petal_width":1.4})