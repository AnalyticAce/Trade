from .setting import Settings
from .debug import Debugger

class Trader:
    def __init__(self):
        self.bot_settings = Settings()
        self.prices = {'sell': [], 'buy': []}
        self.debug = Debugger()

    def run(self):
        while True:
            try:
                command = input().strip()
                if command:
                    self.parse(command)
            except EOFError:
                break

    def parse(self, command):
        parts = command.split(' ')
        if parts[0] == 'settings':
            self.bot_settings.update_settings(parts[1:])
        elif parts[0] == 'update' and parts[1] == 'game':
            self.bot_settings.update_game(parts[2:])
        elif parts[0] == 'action' and parts[1] == 'order':
            self.make_decision()

    def make_decision(self):
        for pair, data in self.bot_settings.market_data.data.items():
            closing_prices = data['close']
            if closing_prices:
                base_currency, quote_currency = pair.split('_')
                dollars = self.bot_settings.stack.get(base_currency, 0)
                sell_fig = self.bot_settings.stack.get(quote_currency, 0)
                asset = dollars + (sell_fig * closing_prices[-1])
                self.debug.print(f"Total Assets: ${asset:.2f} 💰")
                self.bot_settings.market_data.buy_or_sell_signal(pair, dollars, sell_fig, asset)
