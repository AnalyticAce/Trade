import statistics
from math import sqrt

class Indicators:
    def __init__(self):
        self.data = {}

    def standard_deviation(self, array, period):
        """
        Calculate the standard deviation of a given array over a specified period.

        The standard deviation is a measure of the dispersion of values in a dataset from its mean. 
        It is calculated by:
        1. Computing the mean of the last 'period' elements
        2. Calculating squared differences from the mean
        3. Taking the square root of the average squared difference

        Parameters
        ----------
        array : list or array-like
            The input array of numerical values
        period : int
            The number of elements to consider for the calculation

        Returns
        -------
        float or None
            The standard deviation value if array length is sufficient,
            None if array length is less than specified period

        Examples
        --------
        >>> sd = Indicators()
        >>> array = [1, 2, 3, 4, 5]
        >>> sd.standard_deviation(array, 3)
        0.816496580927726
        """
        if len(array) < period:
            return None
        deviation_sum = 0
        average = statistics.mean(array[-period:])
        for i in array[-period:]:
            deviation_sum += pow((abs(i - average)), 2)
        return sqrt(deviation_sum / period)

    def moving_average(self, array, period):
        """
        Calculate the Simple Moving Average (SMA) for a given array over a specified period.

        Parameters:
            array (list): A list of numerical values to calculate the moving average from.
            period (int): The number of periods to consider for the moving average calculation.

        Returns:
            float or None: The calculated moving average value if the array length is sufficient,
                        None if the array length is less than the specified period.

        Example:
            >>> arr = [1, 2, 3, 4, 5]
            >>> moving_average(arr, 3)
            4.0
        """
        if len(array) < period:
            return None
        return sum(array[-period:]) / period
    
    def smoothed_moving_average(self, array, period):
        """
        Calculate the Smoothed Moving Average (SMMA) for a given array.

        The SMMA is a variation of the Simple Moving Average (SMA) that gives more weight to recent data.
        First value is calculated as SMA, subsequent values use the formula:
        SMMA(current) = (SMMA(previous) * (period - 1) + current_price) / period

        Parameters:
            array (list): List of numerical values to calculate SMMA for.
            period (int): Number of periods to use in the calculation.

        Returns:
            list: List containing the SMMA values. Returns None if array length is less than period.
            
        Example:
            >>> data = [1, 2, 3, 4, 5, 6, 7]
            >>> smoothed_moving_average(data, 3)
            [2.0, 2.67, 3.78, 4.85, 5.9]
        """
        if len(array) < period:
            return None
        smoothed = [sum(array[:period]) / period]
        for i in range(period, len(array)):
            smoothed.append((smoothed[-1] * (period - 1) + array[i]) / period)
        return smoothed

    def exponential_moving_average(self, pair, window):
        """Calculate and store Exponential Moving Average (EMA) for a given trading pair.

        The EMA gives more weight to recent data points, making it more responsive to new
        information compared to a simple moving average (SMA).

        Parameters:
            pair (str): Trading pair identifier (e.g., 'BTC/USD')
            window (int): Number of periods to consider for the EMA calculation

        Returns:
            None: Results are stored in self.data[pair]["ema"]

        Notes:
            - Requires at least 'window' number of closing prices to begin calculation
            - Uses the formula: EMA = Price(t) * k + EMA(y) * (1-k)
              where k = 2/(window + 1)
            - First EMA value is calculated as simple average of initial window
        """
        closes = self.data[pair]["close"]
        if len(closes) < window:
            return
        k = 2 / (window + 1)
        ema = statistics.mean(closes[:window])
        for i in range(window, len(closes)):
            ema = closes[i] * k + ema * (1 - k)
            self.data[pair]["ema"].append(ema)

    def ADX_indicator(self, pair, period=14):
        """
        Calculate the Average Directional Index (ADX), +DI, and -DI indicators.
        The ADX measures trend strength without regard to trend direction. Higher values
        indicate stronger trends, while lower values indicate weaker trends or ranging markets.
        The +DI and -DI indicators help determine trend direction.
        Parameters:
        ----------
        pair : str
            The trading pair symbol for which to calculate the ADX
        period : int, optional
            The time period for calculations (default is 14)
        Returns:
        -------
        tuple[float | None, float | None, float | None]
            A tuple containing:
            - ADX value (0-100): Strength of the trend
            - +DI value (0-100): Positive directional indicator
            - -DI value (0-100): Negative directional indicator
            Returns (None, None, None) if insufficient data
        Notes:
        -----
        The calculation includes:
        1. True Range (TR)
        2. Directional Movement (DM)
        3. Smoothed Moving Averages of TR and DM
        4. Directional Indicators (DI)
        5. Directional Index (DX)
        6. Average Directional Index (ADX)
        """
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
        """
        Calculate Bollinger Bands for a given trading pair.

        Bollinger Bands consist of a middle band (simple moving average) with upper and lower bands
        that are standard deviations away from the middle band.

        Parameters
        ----------
        pair : str
            The trading pair symbol to calculate Bollinger Bands for
        period : int, optional
            The time period for the moving average calculation (default is 20)
        deviation : int, optional
            Number of standard deviations for the upper/lower bands (default is 2)

        Returns
        -------
        tuple or (None, None, None)
            A tuple containing:
            - upper band (float or None)
            - middle band/SMA (float or None)  
            - lower band (float or None)
            Returns (None, None, None) if insufficient data or calculation fails

        Notes
        -----
        Requires at least 'period' number of data points to calculate.
        Uses closing prices for calculations.
        """
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