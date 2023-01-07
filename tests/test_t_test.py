import biostats as bs

def test_one_sample_t_test():
    data = bs.dataset("one_sample_t_test.csv")
    summary, result = bs.one_sample_t_test(data=data, variable="Angle", expect=120, kind="two-side")

def test_two_sample_t_test():
    data = bs.dataset("two_sample_t_test.csv")
    summary, result = bs.two_sample_t_test(data=data, variable="Value", between="Time", group=["2pm", "5pm"], kind="equal variances")

def test_paired_t_test():
    data = bs.dataset("paired_t_test.csv")
    summary, result = bs.paired_t_test(data=data, variable="Length", between="Feather", group=["Typical", "Odd"], pair="Bird")

def test_pairwise_t_test():
    data = bs.dataset("pairwise_t_test.csv")
    summary, result = bs.pairwise_t_test(data=data, variable="Length", between="Location")