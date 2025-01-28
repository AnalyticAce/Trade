from math import sqrt, pow

class LinearRegression:
    """A class for performing simple linear regression analysis.
    This class implements linear regression to find the best-fitting line through a set of points
    using the least squares method. It can calculate the slope and intercept of the regression line,
    compute the root mean square error (RMSE), and make predictions.
    Parameters
    ----------
    close : array-like
        The dependent variable values (y-coordinates).
    period : int
        The number of time periods to consider for the regression.
    Methods
    -------
    calculate_m_b()
        Calculates and returns the slope (m) and y-intercept (b) of the regression line.
    rmse(a, b, first=True)
        Calculates the Root Mean Square Error of the regression line.
    predictive_value(a, b, year)
        Predicts the y-value for a given x-value using the regression line.
    Examples
    --------
    >>> prices = [100, 102, 104, 103, 106]
    >>> regression = LinearRegression(close=prices, period=5)
    >>> slope, intercept = regression.calculate_m_b()
    >>> predicted_value = regression.predictive_value(slope, intercept, 6)
    """
    def __init__(self, close, period):
        self.close = close
        self.period = period
    
    def calculate_m_b(self):
        """
        Calculates the slope (m) and y-intercept (b) of a linear regression line.

        The method uses the least squares method to find the best fitting line
        through a set of points, where x-coordinates are the indices (0 to period-1)
        and y-coordinates are the closing prices.

        Returns:
            tuple: A tuple containing:
                - a (float): The slope (m) of the regression line
                - b (float): The y-intercept (b) of the regression line

        The line equation is of the form: y = ax + b

        Formula used:
            a = (n∑xy - ∑x∑y) / (n∑x² - (∑x)²)
            b = (∑y - a∑x) / n

        where:
            n is the period
            x are the indices from 0 to period-1
            y are the closing prices
        """
        dem = (self.period * sum(pow(x, 2) for x in range(self.period)) - pow(sum(range(self.period)), 2))
        num = (self.period * sum(x * y for x, y in zip(range(self.period), self.close)) - sum(range(self.period)) * sum(self.close))
        a = num / dem
        b = (sum(self.close) - a * sum(range(self.period))) / self.period
        a /= 1
        b /= 1
        return a, b

    def rmse(self, a, b, first=True):
        """Calculate the Root Mean Square Error (RMSE) between actual and predicted values.

        This method computes RMSE either by:
        1. Comparing actual close prices to a linear prediction (y = ax + b) when first=True
        2. Comparing actual indices to predicted x-coordinates when first=False

        Parameters
        ----------
        a : float
            Slope coefficient of the linear equation
        b : float
            Y-intercept of the linear equation
        first : bool, optional
            If True, calculates RMSE for y-values (close prices)
            If False, calculates RMSE for x-values (indices)
            Default is True

        Returns
        -------
        float
            The calculated RMSE value

        Notes
        -----
        The RMSE is calculated as sqrt(sum(squared_differences) / n) where n is the number 
        of data points in self.close
        """
        diff = 0
        for i in range(len(self.close)):
            if first:
                diff += (self.close[i] - (a * i + b)) ** 2
            else:
                predicted_X = (-b + self.close[i]) / a
                diff += (i - predicted_X) ** 2
        res = (diff / len(self.close)) ** 0.5
        return res

    def predictive_value(self, a, b, period):
        """
        Calculate the predictive value using a linear function.

        Computes the predicted value based on the linear equation y = ax + b,
        where 'period' is the x value.

        Args:
            a (float): Slope coefficient of the linear function
            b (float): Y-intercept of the linear function
            period (float): The x value for which to calculate the prediction

        Returns:
            float: The predicted y value for the given period
        """
        return a * period + b