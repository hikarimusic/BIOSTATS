---
title: 'BIOSTATS: An intuitive app for statistical analysis'
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

Scientific research relies on statistical analysis to reach a conclusion from experimental results. Commonly used statistical software (e.g. R, SAS, SPSS, STATA) often require the usage of software-specific commands which can overwhelm researchers with little experience in programming, and sometimes include too many functionalities which may confuse researchers with only basic statistical knowledge. Therefore, a coding-free statistical software with concise yet comprehensive functionalities is in demand.

We present ``BIOSTATS``, an intuitive app for statistical analysis. With a straight-forward graphical user interface, researchers can perform various statistical analyses with only a few clicks. ``BIOSTATS`` contains most of the commonly-used statistical (especially biostatistical) tests including t-test, chi-square test, ANOVA, regression, nonparametric methods, to name just a few. It can also generate statistical graphics of various types, enabling the visualization of relations between different variables. Users can import data and save results in different formats, as well as edit the data directly in the software. Designed based on the principle of simplicity, all of the functions in ``BIOSTATS`` should be intuitive enough for users to use without instructions. BIOSTATS is also a Python package hosted on PyPI, which has a fully-featured API and can be easily integrated into other projects.

``BIOSTATS`` is free, open-source and well-documented on the official website. It is written in Python and exploits various free packages including ``pandas``, ``numpy``, ``scipy``, ``statsmodels``, ``scikit-learn``, ``matplotlib``, and ``seaborn``. We refer to multiple textbooks [@mcdonald2009handbook] [@rosner2015fundamentals] and websites [mangiafico_2015] [bobbitt_2022] [ucla_2021] for the related theories and mathematics when developing ``BIOSTATS``.

# References