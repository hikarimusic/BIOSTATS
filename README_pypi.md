# __What is BIOSTATS__

* BIOSTATS is an intuitive app for statistical analysis.
* It is free and open-source.
* It works on _Windows_ / _Linux_.

### __BIOSTATS includes these tests:__

| Basic | t-Test | ANOVA | Exact Test | Chi-Square Test |
|---|---|---|---|---|
| Numeric | One-Sample t-Test | One-Way ANOVA | Binomial Test | Chi-Square Test |
| Numeric (Grouped) | Two-Sample t-Test | Two-Way ANOVA | Fisher's Exact Test | Chi-Square Test (Fit) |
| Categorical | Paired t-Test | One-Way ANCOVA | McNemar's Exact Test | McNemar's Test |
| Contingency | Pairwise t-Test | Two-Way ANCOVA |  | Mantel-Haenszel Test |
|  |  | Multivariate ANOVA |  |  |
|  |  | Repeated Measures ANOVA |  |  |

---

| Linear Regression | Logistic Regression | Nonparametric | Others |
|---|---|---|---|
| Correlation | Simple Logistic Regression | Sign Test | Screening Test |
| Correlation Matrix | Multiple Logistic Regression | Median Test | Epidemiologic Study |
| Simple Linear Regression | Ordered Logistic Regression | Wilcoxon Signed-Rank Test | Factor Analysis |
| Multiple Linear Regression | Multinomial Logistic Regression | Wilcoxon Rank-Sum Test | Principal Component Analysis |
|  |  | Kruskal-Wallis Test | Linear Discriminant Analysis |
|  |  | Friedman Test |  |
|  |  | Spearman's Rank Correlation |  |

### __BIOSTATS includes these plots:__

| Distribution | Categorical | Relational | Multiple | Others |
|---|---|---|---|---|
| Histogram | Count Plot | Scatter Plot | Ultimate Plot | Heatmap |
| Density Plot | Strip Plot | Line Plot | Pair Plot | FA Plot |
| Cumulative Plot | Swarm Plot | Regression Plot | Joint Plot | PCA Plot |
| 2D Histogram | Box Plot |  |  | LDA Plot |
| 2D Density Plot | Boxen Plot |  |  |  |
|  | Violin Plot |  |  |  |
|  | Bar Plot |  |  |  |

# __Quick Start__

### __Install Package__

You can install the package from pip:

```sh
pip install biostatistics
```

The main window can be called directly:

```sh
biostats
```

You can also import _biostats_ and use the functions:

```sh
:~$ python3
>>> import biostats as bs
>>> data = bs.dataset("one_way_anova.csv")
>>> summary, result = bs.one_way_anova(data=data, variable="Length", between="Location")
>>> summary
     Location  Count      Mean  Std. Deviation  95% CI: Lower  95% CI: Upper
1   Tillamook     10  0.080200        0.011963       0.071642       0.088758
2     Newport      8  0.074800        0.008597       0.067613       0.081987
3  Petersburg      7  0.103443        0.016209       0.088452       0.118434
4     Magadan      8  0.078012        0.012945       0.067190       0.088835
5   Tvarminne      6  0.095700        0.012962       0.082098       0.109302
>>> result
          D.F.  Sum Square  Mean Square  F Statistic   p-value     
Location     4    0.004520     0.001130     7.121019  0.000281  ***
Residual    34    0.005395     0.000159          NaN       NaN  NaN
```

# __More__

More information can be found on the official website.

* https://hikarimusic.github.io/BIOSTATS/

If you have any suggestion or find any bug, please contach me. We need your help!

* Contact me: hikarimusic.tm@gmail.com

If you use BIOSTATS in your research, it's a good idea to cite the paper of BIOSTATS.

* Citation: _working_

#### __References__:

McDonald, John H. _Handbook of biological statistics_. Vol. 2. Baltimore, MD: sparky house publishing, 2009.

Mangiafico, Salvatore S. "An R companion for the handbook of biological statistics." _Available: rcompanion.org/documents/RCompanionBioStatistics.pdf.(January 2016)_ (2015).

Rosner, Bernard. _Fundamentals of biostatistics_. Cengage learning, 2015.

Zach. _Statology_. 2021, www.statology.org.

UCLA. _Statistical Methods and Data Analytics_. 2021, stats.oarc.ucla.edu.
