import sys
from .debug import Debugger
from .model import LinearRegression
from .indicators import Indicators

class MarketData(Indicators):
    """
    A class for managing market data and trading operations.
    This class extends the Indicators class and provides functionality for:

    - Storing and managing market data for different trading pairs
    - Executing buy/sell orders
    - Implementing money management strategies
    - Calculating technical indicators
    - Generating trading signals
    
    Attributes:
        data (dict): Dictionary storing market data for different trading pairs
        list_buys (list): List tracking buy orders
        list_sells (list): List tracking sell orders
        debug (Debugger): Debugger instance for logging
        trade_history (list): List storing historical trade records

    Methods:
        add_data: Add market data for a specific trading pair
        order: Execute and record a trade order
        money_management: Manage trading decisions based on asset value
        indicators_signal: Calculate technical indicators for a trading pair
        buy_or_sell_signal: Generate trading signals based on technical analysis
        >>> market = MarketData()
        >>> market.add_data('BTC/USD', datetime.now(), 50000.0, 49000.0, 49500.0, 49800.0, 100.5)
        >>> market.order('buy', 'BTC/USD', 0.5)

    """
    def __init__(self):
        self.data = {}
        self.list_buys = []
        self.list_sells = []
        self.debug = Debugger()
        self.trade_history = []

    def add_data(self, pair, date, high, low, open_p, close, volume):
        """
        Add market data for a specific trading pair.

        This method adds price and volume data for a given trading pair to the market data structure.
        If the pair doesn't exist in the data dictionary, it initializes the data structure for that pair
        with empty lists for various technical indicators.

        Args:
            pair (str): The trading pair identifier (e.g., 'BTC/USD')
            date (datetime): The timestamp for the data point
            high (float): The highest price during the period
            low (float): The lowest price during the period  
            open_p (float): The opening price for the period
            close (float): The closing price for the period
            volume (float): The trading volume for the period

        Returns:
            None

        Example:
            market.add_data('BTC/USD', datetime.now(), 50000.0, 49000.0, 49500.0, 49800.0, 100.5)
        """
        if pair not in self.data:
            self.data[pair] = {
                'date': [],
                'high': [],
                'low': [],
                'open': [],
                'close': [],
                'volume': [],
                'bollinger': {'upper': [], 'lower': []},
                'ema': [],
                'mcginley': []
            }
        self.data[pair]['date'].append(date)
        self.data[pair]['high'].append(high)
        self.data[pair]['low'].append(low)
        self.data[pair]['open'].append(open_p)
        self.data[pair]['close'].append(close)
        self.data[pair]['volume'].append(volume)

    def order(self, action, pair, amount):
        """
        Executes a trade order and records it in the trade history.

        This method simulates placing a buy or sell order for a given trading pair and amount.
        It prints the order details and stores the transaction in the trade history.

        Args:
            action (str): The type of order - either "buy" or "sell"
            pair (str): The trading pair symbol (e.g., "BTC/USD")
            amount (float): The quantity to buy or sell

        Returns:
            None

        Example:
            >>> market.order("buy", "BTC/USD", 0.5)
            buy BTC/USD 0.5
        """
        print(f'{action} {pair} {amount}', flush=True)
        if action == "buy":
            self.trade_history.append(("buy", pair, amount, self.data[pair]['close'][-1]))
        elif action == "sell":
            self.trade_history.append(("sell", pair, amount, self.data[pair]['close'][-1]))

    def money_management(self, pair, sell_stack, buy_stack, asset):
        """
        Manages trading decisions based on asset value and trading stack status.

        This method implements a basic money management strategy by enforcing take profit 
        and stop loss rules based on asset value thresholds.

        Parameters:
            pair (str): The trading pair symbol (e.g., 'BTC/USD')
            sell_stack (float): The amount to sell in the trade
            buy_stack (float): The amount to buy in the trade
            asset (float): Current asset value

        Returns:
            bool: True if a trade was executed (either take profit or stop loss),
                False if no trade was executed

        Details:
            - Takes profit when asset value >= 1500 and there are open buy positions
            - Stops loss when asset value <= 800 and there are open buy positions
            - Clears buy positions and records sell operations after execution
        """
        if asset >= 1500 and len(self.list_buys) > 0:
            self.order("sell", pair, sell_stack)
            self.debug.print(f"Selling due to take profit: {self.list_buys}, Asset: {asset}")
            self.list_sells.append("sell")
            self.list_buys.clear()
            return True

        if asset <= 800 and len(self.list_buys) > 0:
            self.order("sell", pair, sell_stack)
            self.debug.print(f"Selling due to stop loss: {self.list_buys}, Asset: {asset}")
            self.list_sells.append("sell")
            self.list_buys.clear()
            return True

        return False

    def indicators_signal(self, pair):
        """
        Calculate and return various technical indicators for a given trading pair.
        This method computes several technical analysis indicators including:
        - Simple Moving Average (SMA)
        - Linear Regression prediction
        - ADX (Average Directional Index) components
        - Bollinger Bands
        - Exponential Moving Average (EMA)
        Parameters
        ----------
        pair : str
            The trading pair symbol to calculate indicators for (e.g. 'BTC/USD')
        Returns
        -------
        tuple
        A tuple containing the following indicators in order:
            - em50 (float): 50-period Simple Moving Average
            - prediction (float): Linear regression predicted value
            - DIplus (float): Positive Directional Indicator
            - DIminus (float): Negative Directional Indicator 
            - upper (float): Upper Bollinger Band
            - lower (float): Lower Bollinger Band
            - ema50_r (float): 50-period Exponential Moving Average
        """
        close_prices = self.data[pair]['close']
        lr = LinearRegression(close_prices, len(close_prices))
        a, b = lr.calculate_m_b()
        prediction = lr.predictive_value(a, b, len(close_prices) + 1)
        rmse = lr.rmse(a, b)
        
        em50 = self.smoothed_moving_average(close_prices, 50)
        ADX, DIplus, DIminus = self.ADX_indicator(pair, 100)
        upper, _, lower = self.bollinger_bands(pair, 20, 2)
        ema50_r = self.exponential_moving_average(pair, 50)
        
        return em50, prediction, DIplus, DIminus, upper, lower, ema50_r

    def buy_or_sell_signal(self, pair, buy_stack, sell_stack, asset):
        """
        Determines whether to buy or sell based on technical indicators and current market conditions.

        Args:
            pair (str): The trading pair to analyze (e.g., 'BTC/USD')
            buy_stack (float): Available funds for buying
            sell_stack (float): Available assets for selling
            asset (str): The asset being traded

        Returns:
            None: Function returns early if money management conditions are met
                or prints "no_moves" if no trade signal is generated

        The function uses multiple technical indicators to generate buy/sell signals:
        - EMA50 (50-period Exponential Moving Average)
        - Price predictions
        - Directional Indicators (DI+ and DI-)
        - Bollinger Bands (Upper and Lower bands)

        Buy signals are generated when:
        - Price is above lower band
        - DI+ is greater than DI-
        - Predicted price is higher than current price
        - EMAs show upward momentum
        OR
        - When sell_stack is zero (forced buy condition)

        Sell signals are generated when:
        - Price is below upper band
        - Predicted price is lower than current price
        - DI+ is less than DI-
        - EMAs show downward momentum
        """
        if self.money_management(pair, sell_stack, buy_stack, asset):
            return

        em50, prediction, DIplus, DIminus, upper, lower, ema50_r = self.indicators_signal(pair)

        if None in em50:
            print("no_moves", flush=True)
            return

        current_price = self.data[pair]['close'][-1]
        can_buy = buy_stack / current_price / 1

        if len(self.list_buys) > 0 or len(self.list_sells) > 0:
            print("no_moves", flush=True)
            return

        if current_price > lower and DIplus > DIminus \
            and prediction > current_price and em50[-1] > em50[-2] \
            and ema50_r[-1] > ema50_r[-2]:
            self.list_buys.append("buy")
            self.debug.print(f"Buying: {len(self.list_buys)}")
            self.order("buy", pair, can_buy)
        elif sell_stack == 0:
            self.list_buys.append("buy")
            self.debug.print(f"Buying due to zero sell stack: {self.list_buys}")
            self.order("buy", pair, can_buy)
        elif current_price < upper and prediction < current_price \
            and DIplus < DIminus and em50[-1] < em50[-2] and ema50_r[-1] < ema50_r[-2]:
            self.list_sells.append("sell")
            self.debug.print(f"Selling: {len(self.list_sells)}")
            self.order("sell", pair, sell_stack)
        else:
            print("no_moves", flush=True)
