---
title: 'BIOSTATS: A User-Friendly Application for Statistical Analysis'
tags:
  - python
  - data-science
  - statistics
  - data-visualization
  - gui-application
authors:
  - name: Yeu-Guang Tung
    orcid: 0000-0003-3671-5334
    affiliation: 1
affiliations:
  - name: School of Medicine, National Taiwan University, Taiwan
    index: 1
date: 7 January 2023
bibliography: paper.bib
---

# Summary

``BIOSTATS`` is a user-friendly statistical software application with a graphical user interface (GUI) that allows researchers to easily perform a wide range of statistical tests without the need for coding. The tests offered include t-tests, chi-square tests, ANOVA, linear and logistic regression, nonparametric methods, and descriptive statistics. BIOSTATS also allows users to visualize relationships between variables through statistical graphics. It is suitable for researchers and data scientists in various fields, and is available as a Python package on PyPI with a fully-featured API for integration into other projects. It was originally designed for biostatistics but can be applied to a wide range of statistical topics.

# Statement of need

Scientific research often relies on statistical analysis to draw conclusions from experimental results. However, many commonly used statistical software programs, such as R, SAS, SPSS, and STATA, require the use of software-specific commands that can be challenging for researchers with limited programming experience. Additionally, these programs often have a large number of features that may be confusing for researchers who only have basic statistical knowledge. As a result, there is a need for statistical software that is easy to use and has concise, comprehensive functionality without the need for coding.

We introduce ``BIOSTATS``, a user-friendly application for statistical analysis. Its straightforward and intuitive graphical user interface allows researchers to easily perform a wide range of statistical tests with just a few clicks, eliminating the need to enter commands. These tests include t-tests, chi-square tests, ANOVA, linear and logistic regression, nonparametric methods, and descriptive statistics, among others. ``BIOSTATS`` also allows users to visualize relationships between variables by generating various statistical graphics, and allows for the import, export, and direct editing of data within the software. Designed with simplicity in mind, ``BIOSTATS`` is intuitive enough to use without the need for instructions, and is suitable for researchers and data scientists in a variety of fields. Originally developed for use in biostatistics, ``BIOSTATS`` can also be applied to a wide range of statistical topics. In addition, it is available as a Python package on PyPI, which includes a fully-featured API for easy integration into other projects.

``BIOSTATS`` is a free and open-source software that is well-documented on the official website. It is implemented in Python and utilizes a range of open-source packages, including ``pandas``, ``numpy``, ``scipy``, ``statsmodels``, ``scikit-learn``, ``matplotlib``, and ``seaborn``. The development of ``BIOSTATS`` is guided by a thorough review of statistical theories and mathematical principles from various sources, including textbooks [@mcdonald2009handbook] [@rosner2015fundamentals] and online resources [@mangiafico_2015] [@bobbitt_2022] [@ucla_2021].

# References