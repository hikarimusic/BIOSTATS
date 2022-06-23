from .basic import numeral, numeral_grouped, categorical,contingency
from .t_test import one_sample_t_test
from .anova import one_way_anova
from .exact_test import binomial_test, fisher_exact_test
from .chi_square import chi_square_test, chi_square_test_fit
from .linear_regression import simple_linear_regression
from .logistic_regression import simple_logistic_regression
from .non_parametric import kruskal_wallis_test
from .distribution_plot import histogram, density_plot, cumulative_plot, histogram_2D, density_plot_2D
from .categorical_plot import count_plot, strip_plot, swarm_plot, box_plot, boxen_plot, violin_plot, bar_plot
from .relational_plot import scatter_plot, line_plot, regression_plot
from .multiple_plot import ultimate_plot, pair_plot, joint_plot