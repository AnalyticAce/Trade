from .market import MarketData

class Settings:
    """A class to manage game settings and market data for a trading bot.

    This class handles the initialization, updates, and storage of various game parameters
    including time constraints, candle information, initial stack values, and market data.

    Attributes:
        time_bank (int): Current time bank value in milliseconds.
        max_time_bank (int): Maximum allowed time bank in milliseconds.
        time_per_move (int): Time allowed per move in milliseconds.
        candle_interval (int): Time interval between candles in seconds.
        candle_format (list): Format specification for candle data.
        candles_total (int): Total number of candles in the game.
        candles_given (int): Number of candles provided so far.
        initial_stack (float): Initial amount of currency available.
        transaction_fee_percent (float): Fee percentage for each transaction.
        stack (dict): Current amounts of different currencies.
        market_data (MarketData): Object storing market data information.

    Methods:
        update_settings(settings): Updates game settings based on key-value pairs.
        update_game(updates): Updates game state including candles and stack information.
    """
    def __init__(self):
        self.time_bank = 0
        self.max_time_bank = 0
        self.time_per_move = 1
        self.candle_interval = 1
        self.candle_format = []
        self.candles_total = 0
        self.candles_given = 0
        self.initial_stack = 0
        self.transaction_fee_percent = 0
        self.stack = {}
        self.market_data = MarketData()

    def update_settings(self, settings):
        """
        Updates the trading bot settings based on key-value pairs.

        Args:
            settings (list): A list containing two elements [key, value] where:
                - key (str): Setting name to update
                - value (str): New value for the setting

        Supported settings:
            - candle_interval: Time in seconds between candles (int)
            - candle_format: Comma-separated list of candle data fields (list)
            - candles_total: Total number of candles in the dataset (int) 
            - candles_given: Number of candles given per update (int)
            - initial_stack: Starting amount of money (float)
            - transaction_fee_percent: Fee percentage per transaction (float)
            - timebank: Initial and maximum time bank in milliseconds (int) 
            - time_per_move: Time allowed per move in milliseconds (int)

        Returns:
            None
        """
        key, value = settings[0], settings[1]
        if key == 'candle_interval':
            self.candle_interval = int(value)
        elif key == 'candle_format':
            self.candle_format = value.split(',')
        elif key == 'candles_total':
            self.candles_total = int(value)
        elif key == 'candles_given':
            self.candles_given = int(value)
        elif key == 'initial_stack':
            self.initial_stack = float(value)
        elif key == 'transaction_fee_percent':
            self.transaction_fee_percent = float(value)
        elif key == 'timebank':
            self.time_bank = int(value)
            self.max_time_bank = int(value)
        elif key == 'time_per_move':
            self.time_per_move = int(value)

    def update_game(self, updates):
        """
        Updates game state with new market data and stack information.

        This method processes two types of updates:
        1. 'next_candles': Updates market data with new candle information
        2. 'stacks': Updates currency stack amounts

        Parameters
        ----------
        updates : list
            A list containing update type and data.
            For 'next_candles': [type, candle_string] where candle_string contains semicolon-separated candles
            For 'stacks': [type, stack_string] where stack_string contains comma-separated currency:amount pairs

        Each candle string format: pair,date,high,low,open,close,volume
        Each stack string format: currency1:amount1,currency2:amount2,...

        Returns
        -------
        None

        Updates
        -------
        self.market_data : MarketData
            Updates with new candle data when processing 'next_candles'
        self.stack : dict
            Updates currency amounts when processing 'stacks'
        """
        if updates[0] == 'next_candles':
            candles = updates[1].split(';')
            for candle in candles:
                data = candle.split(',')
                pair, date, high, low, open_p, close, volume = data
                date, high, low, open_p, close, volume = map(float, [date, high, low, open_p, close, volume])
                self.market_data.add_data(pair, date, high, low, open_p, close, volume)
        elif updates[0] == 'stacks':
            stacks = updates[1].split(',')
            for stack in stacks:
                currency, amount = stack.split(':')
                self.stack[currency] = float(amount)
