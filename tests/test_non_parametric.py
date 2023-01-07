import biostats as bs

def test_median_test():
    data = bs.dataset("median_test.csv")
    summary, result = bs.median_test(data=data, variable="Value", expect=3)

def test_sign_test():
    data = bs.dataset("sign_test.csv")
    summary, result = bs.sign_test(data=data, variable="Concentration", between="Month", group=["August", "November"], pair="Clone")

def test_wilcoxon_signed_rank_test():
    data = bs.dataset("wilcoxon_signed_rank_test.csv")
    summary, result = bs.wilcoxon_signed_rank_test(data=data, variable="Concentration", between="Month", group=["August", "November"], pair="Clone")

def test_wilcoxon_rank_sum_test():
    data = bs.dataset("wilcoxon_rank_sum_test.csv")
    summary, result = bs.wilcoxon_rank_sum_test(data=data, variable="Value", between="Time", group=["2pm", "5pm"])

def test_kruskal_wallis_test():
    data = bs.dataset("kruskal_wallis_test.csv")
    summary, result = bs.kruskal_wallis_test(data=data, variable="Value", between="Group")

def test_friedman_test():
    data = bs.dataset("friedman_test.csv")
    summary, result = bs.friedman_test(data=data, variable="response", between="drug", subject="patient")

def test_spearman_rank_correlation():
    data = bs.dataset("spearman_rank_correlation.csv")
    summary, result = bs.spearman_rank_correlation(data=data, x="Volume", y="Pitch")