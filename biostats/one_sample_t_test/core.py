import math
from scipy import stats
from scipy.stats import t

class Model:
    
    def __init__(self):
        
        self.data = []

    def update(self, data):

        self.data.clear()
        self.data = data



