from .market import MarketData

class Settings:
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
