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
                self.std.append("N.A.")
            else:
                self.std.append(stats.tstd(self.data[i]))

        self.var = []
        for i in range(len(self.group)):
            if len(self.data[i]) == 1:
                self.var.append("N.A.")
            else:
                self.var.append(stats.tvar(self.data[i]))

        self.min = []
        for i in range(len(self.group)):
            self.min.append(stats.tmin(self.data[i]))

        self.max = []
        for i in range(len(self.group)):
            self.max.append(stats.tmax(self.data[i]))

        self.range = []
        for i in range(len(self.group)):
            self.range.append(stats.tmax(self.data[i])-stats.tmin(self.data[i]))

        '''
        self.sem = []
        for i in range(len(self.group)):
            self.sem.append(stats.tsem(self.data[i]))
        '''


