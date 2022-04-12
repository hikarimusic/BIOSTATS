import math
import numpy as np
from scipy import stats
from scipy.stats import t

class Model:
    
    def __init__(self):
        
        self.data = []
        self.group = []

    def update(self):

        self.size = []
        for i in range(len(self.group)):
            self.size.append(len(self.data[i]))

        self.mean = []
        for i in range(len(self.group)):
            self.mean.append(stats.tmean(self.data[i]))

        self.median = []
        for i in range(len(self.group)):
            self.median.append(np.median(self.data[i]))

        self.std = []
        for i in range(len(self.group)):
            if len(self.data[i]) == 1:
                self.std.append("-")
            else:
                self.std.append(stats.tstd(self.data[i]))

        self.var = []
        for i in range(len(self.group)):
            if len(self.data[i]) == 1:
                self.var.append("-")
            else:
                self.var.append(stats.tvar(self.data[i]))

        self.sem = []
        for i in range(len(self.group)):
            if len(self.data[i]) == 1:
                self.sem.append("-")
            else:
                self.sem.append(stats.tsem(self.data[i]))

        '''
        self.range = []
        for i in range(len(self.group)):
            self.range.append(stats.tmax(self.data[i])-stats.tmin(self.data[i]))
        '''


    def CI_cal(self, level):
        self.CI_two = []
        self.CI_one_1 = []
        self.CI_one_2 = []
        alpha = 1 - level
        for i in range(len(self.group)):
            if len(self.data[i]) == 1:
                self.CI_two.append("-")
                self.CI_one_1.append("-")
                self.CI_one_2.append("-")
            else:
                n = len(self.data[i])
                mean = stats.tmean(self.data[i])
                sem = stats.tsem(self.data[i])

                CI1 = t.ppf(alpha/2, n-1, mean, sem)
                CI2 = t.ppf(1-alpha/2, n-1, mean, sem)
                self.CI_two.append((CI1, CI2))

                CI = t.ppf(alpha, n-1, mean, sem)
                self.CI_one_1.append(CI)

                CI = t.ppf(1-alpha, n-1, mean, sem)
                self.CI_one_2.append(CI)

    def percent_cal(self, percent):
        self.percent = []
        for i in range(len(self.group)):
            self.percent.append(np.percentile(self.data[i], percent))

        self.min = []
        for i in range(len(self.group)):
            self.min.append(np.percentile(self.data[i], 0))

        self.per_25 = []
        for i in range(len(self.group)):
            self.per_25.append(np.percentile(self.data[i], 25))

        self.per_50 = []
        for i in range(len(self.group)):
            self.per_50.append(np.percentile(self.data[i], 50))

        self.per_75 = []
        for i in range(len(self.group)):
            self.per_75.append(np.percentile(self.data[i], 75))

        self.max = []
        for i in range(len(self.group)):
            self.max.append(np.percentile(self.data[i], 100))



