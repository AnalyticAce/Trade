import statistics
from math import sqrt

class Indicators:
    def __init__(self):
        self.data = {}

    def standard_deviation(self, array, period):
        if len(array) < period:
            return None
        deviation_sum = 0
        average = statistics.mean(array[-period:])
        for i in array[-period:]:
            deviation_sum += pow((abs(i - average)), 2)
        return sqrt(deviation_sum / period)

    def moving_average(self, array, period):
        if len(array) < period:
            return None
        return sum(array[-period:]) / period
    
    def smoothed_moving_average(self, array, period):
        if len(array) < period:
            return None
        smoothed = [sum(array[:period]) / period]
        for i in range(period, len(array)):
            smoothed.append((smoothed[-1] * (period - 1) + array[i]) / period)
        return smoothed

    def exponential_moving_average(self, pair, window):
        closes = self.data[pair]["close"]
        if len(closes) < window:
            return
        k = 2 / (window + 1)
        ema = statistics.mean(closes[:window])
        for i in range(window, len(closes)):
            ema = closes[i] * k + ema * (1 - k)
            self.data[pair]["ema"].append(ema)

    def ADX_indicator(self, pair, period=14):
        high = self.data[pair]['high']
        low = self.data[pair]['low']
        close = self.data[pair]['close']
        if len(close) < period + 1:
            return None, None, None
        TR = []
        DMplus = []
        DMminus = []

        for i in range(1, len(close)):
            TR.append(max(high[i] - low[i], abs(high[i] - close[i - 1]), abs(low[i] - close[i - 1])))
            if high[i] - high[i - 1] > low[i - 1] - low[i]:
                DMplus.append(max(high[i] - high[i - 1], 0))
                DMminus.append(0)
            else:
                DMplus.append(0)
                DMminus.append(max(low[i - 1] - low[i], 0))

        ATR = self.smoothed_moving_average(TR, period)
        ADMP = self.smoothed_moving_average(DMplus, period)
        ADMN = self.smoothed_moving_average(DMminus, period)
        
        if ATR is None or ADMP is None or ADMN is None:
            return None, None, None
        
        DIplus = [(ADMP[i] / ATR[i]) * 100 for i in range(len(ATR))]
        DIminus = [(ADMN[i] / ATR[i]) * 100 for i in range(len(ATR))]
        DX = [(abs(DIplus[i] - DIminus[i]) / abs(DIplus[i] + DIminus[i])) * 100 for i in range(len(DIplus))]
        
        ADX = self.smoothed_moving_average(DX, period)

        return ADX[-1], DIplus[-1], DIminus[-1]
    
    def bollinger_bands(self, pair, period=20, deviation=2):
        closes = self.data[pair]['close']
        if len(closes) < period:
            return None, None, None
        sma = self.moving_average(closes, period)
        std = self.standard_deviation(closes, period)
        if sma is None or std is None:
            return None, None, None
        upper = sma + std * deviation
        lower = sma - std * deviation
        return upper, sma, lower