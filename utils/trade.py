from .setting import Settings
from .debug import Debugger

class Trader:
    """A class that handles trading operations and market decisions.

    This class manages bot settings, price tracking, and trade execution based on market data
    and user commands.

    Attributes:
        bot_settings (Settings): Configuration and settings for the trading bot.
        prices (dict): Dictionary tracking buy and sell prices with list values.
        debug (Debugger): Debugger instance for logging and debugging purposes.

    Methods:
        run(): Main loop that continuously processes user input commands.
        parse(command: str): Parses and processes input commands to update settings or make trades.
        make_decision(): Analyzes market data and makes trading decisions for each currency pair.
    """
    def __init__(self):
        self.bot_settings = Settings()
        self.prices = {'sell': [], 'buy': []}
        self.debug = Debugger()

    def run(self):
        """
        Runs the trading application in interactive mode.

        This method continuously reads commands from standard input and processes them
        until an EOF (End of File) is encountered. Empty lines are ignored.

        The method:
        1. Reads a line from standard input
        2. Strips whitespace from the line
        3. If the line is not empty, passes it to the parse method
        4. Continues until EOF is reached

        Raises:
            EOFError: Handled internally to break the loop when EOF is encountered

        Returns:
            None
        """
        while True:
            try:
                command = input().strip()
                if command:
                    self.parse(command)
            except EOFError:
                break

    def parse(self, command):
        """
        Parse and process incoming commands from the game engine.

        This method handles three types of commands:
        - settings: Updates bot settings using the provided parameters
        - update game: Updates game state information
        - action order: Triggers decision making for the next move

        Args:
            command (str): The command string received from the game engine containing
                        space-separated command parts

        Returns:
            None

        Example:
            >>> parse("settings player_names player1 player2")
            >>> parse("update game round 1")
            >>> parse("action order")
        """
        parts = command.split(' ')
        if parts[0] == 'settings':
            self.bot_settings.update_settings(parts[1:])
        elif parts[0] == 'update' and parts[1] == 'game':
            self.bot_settings.update_game(parts[2:])
        elif parts[0] == 'action' and parts[1] == 'order':
            self.make_decision()

    def make_decision(self):
        """
        Evaluates the trading pairs and makes buy/sell decisions based on market data.

        This method processes each trading pair in the bot's market data, calculating total assets
        and determining trading signals. It performs the following for each pair:
        1. Extracts closing prices
        2. Splits the pair into base and quote currencies
        3. Retrieves current holdings for both currencies
        4. Calculates total assets in dollar value
        5. Determines buy/sell signals based on market conditions

        Returns:
            None

        Side Effects:
            - Updates trading signals through market_data's buy_or_sell_signal method
            - Logs asset values through debug printer
        """
        for pair, data in self.bot_settings.market_data.data.items():
            closing_prices = data['close']
            if closing_prices:
                base_currency, quote_currency = pair.split('_')
                dollars = self.bot_settings.stack.get(base_currency, 0)
                sell_fig = self.bot_settings.stack.get(quote_currency, 0)
                asset = dollars + (sell_fig * closing_prices[-1])
                self.debug.print(f"Total Assets: ${asset:.2f} 💰")
                self.bot_settings.market_data.buy_or_sell_signal(pair, dollars, sell_fig, asset)
