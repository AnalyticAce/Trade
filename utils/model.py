from math import sqrt, pow

class LinearRegression:
    def __init__(self, close, period):
        self.close = close
        self.period = period
    
    def calculate_m_b(self):
        dem = (self.period * sum(pow(x, 2) for x in range(self.period)) - pow(sum(range(self.period)), 2))
        num = (self.period * sum(x * y for x, y in zip(range(self.period), self.close)) - sum(range(self.period)) * sum(self.close))
        a = num / dem
        b = (sum(self.close) - a * sum(range(self.period))) / self.period
        a /= 1
        b /= 1
        return a, b

    def rmse(self, a, b, first=True):
        diff = 0
        for i in range(len(self.close)):
            if first:
                diff += (self.close[i] - (a * i + b)) ** 2
            else:
                predicted_X = (-b + self.close[i]) / a
                diff += (i - predicted_X) ** 2
        res = (diff / len(self.close)) ** 0.5
        return res

    def predictive_value(self, a, b, year):
        return a * year + b