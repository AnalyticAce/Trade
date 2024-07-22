# import sys
# from .debug import Debugger
# from .model import LinearRegression
# from .indicators import Indicators

# class MarketData(Indicators):
#     def __init__(self):
#         self.data = {}
#         self.list_buys = []
#         self.list_sell = []
#         self.debug = Debugger()
#         self.trade_history = []

#     def add_data(self, pair, date, high, low, open_p, close, volume):
#         if pair not in self.data:
#             self.data[pair] = {
#                 'date': [],
#                 'high': [],
#                 'low': [],
#                 'open': [],
#                 'close': [],
#                 'volume': [],
#                 'bollinger': {'upper': [], 'lower': []},
#                 'ema': [],
#                 'mcginley': []
#             }
#         self.data[pair]['date'].append(date)
#         self.data[pair]['high'].append(high)
#         self.data[pair]['low'].append(low)
#         self.data[pair]['open'].append(open_p)
#         self.data[pair]['close'].append(close)
#         self.data[pair]['volume'].append(volume)

#     def order(self, action, pair, amount):
#         print(f'{action} {pair} {amount}', flush=True)
#         # Log the trade
#         if action == "buy":
#             self.trade_history.append(("buy", pair, amount, self.data[pair]['close'][-1]))
#         elif action == "sell":
#             self.trade_history.append(("sell", pair, amount, self.data[pair]['close'][-1]))

#     def money_management(self, pair, sell_stack, asset):
#         if asset >= 1500 and len(self.list_buys) > 0:
#             self.order("sell", pair, sell_stack)
#             self.debug.print(f"Selling due to take profit: {self.list_buys}, Asset: {asset}")
#             self.list_sell.append("sell")
#             self.list_buys.clear()
#             return True

#         if asset <= 800 and len(self.list_buys) > 0:
#             self.order("sell", pair, sell_stack)
#             self.debug.print(f"Selling due to stop loss: {self.list_sell}, Asset: {asset}")
#             self.list_sell.append("sell")
#             self.list_buys.clear()
#             return True

#         # sell tp and sl
#         # elif asset >= 1500 and len(self.list_sell) > 0:
#         #     self.order("buy", pair, sell_stack)
#         #     self.debug.print(f"Buying due to take profit: {self.list_buys}, Asset: {asset}")
#         #     self.list_buys.append("buy")
#         #     self.list_sell.clear()
#         #     return True
        
#         # elif asset <= 800 and len(self.list_sell) > 0:
#         #     self.order("buy", pair, sell_stack)
#         #     self.debug.print(f"Buying due to take profit: {self.list_buys}, Asset: {asset}")
#         #     self.list_buys.append("buy")
#         #     self.list_sell.clear()

#         return False

#     def indicators_signal(self, pair):
#         close_prices = self.data[pair]['close']
#         lr = LinearRegression(close_prices, len(close_prices))
#         a, b = lr.calculate_m_b()
#         prediction = lr.predictive_value(a, b, len(close_prices) + 1)
#         rmse = lr.rmse(a, b)
        
#         em50 = self.smoothed_moving_average(close_prices, 50)
#         ADX, DIplus, DIminus = self.ADX_indicator(pair, 100)
#         upper, _, lower = self.bollinger_bands(pair, 20, 2)
        
#         return em50, prediction, DIplus, DIminus, upper, lower

#     def buy_or_sell_signal(self, pair, buy_stack, sell_stack, asset):
#         if self.money_management(pair, sell_stack, asset):
#             return

#         em50, prediction, DIplus, DIminus, upper, lower = self.indicators_signal(pair)

#         if None in em50:
#             print("no_moves", flush=True)
#             return

#         current_price = self.data[pair]['close'][-1]
#         can_buy = buy_stack / current_price / 1

#         # Block all other signals if a trade is open
#         if len(self.list_buys) > 0 or len(self.list_sell) > 0:
#             print("no_moves", flush=True)
#             return

#         if current_price > lower and DIplus > DIminus and prediction > current_price and em50[-1] > em50[-2]:
#             self.list_buys.append("buy")
#             self.debug.print(f"Buying: {len(self.list_buys)}")
#             self.order("buy", pair, can_buy)
#         elif sell_stack == 0:
#             self.list_buys.append("buy")
#             self.debug.print(f"Buying due to zero sell stack: {self.list_buys}")
#             self.order("buy", pair, can_buy)
#         elif current_price < upper and prediction < current_price and DIplus < DIminus and em50[-1] < em50[-2]:
#             self.list_sell.append("sell")
#             self.debug.print(f"Selling: {len(self.list_sell)}")
#             self.order("sell", pair, sell_stack)
#         else:
#             print("no_moves", flush=True)

import sys
from .debug import Debugger
from .model import LinearRegression
from .indicators import Indicators

class MarketData(Indicators):
    def __init__(self):
        self.data = {}
        self.list_buys = []
        self.list_sells = []
        self.debug = Debugger()
        self.trade_history = []

    def add_data(self, pair, date, high, low, open_p, close, volume):
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
        print(f'{action} {pair} {amount}', flush=True)
        # Log the trade
        if action == "buy":
            self.trade_history.append(("buy", pair, amount, self.data[pair]['close'][-1]))
        elif action == "sell":
            self.trade_history.append(("sell", pair, amount, self.data[pair]['close'][-1]))

    def money_management(self, pair, sell_stack, buy_stack, asset):
        # Take-profit and stop-loss for buy trades
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
        if self.money_management(pair, sell_stack, buy_stack, asset):
            return

        em50, prediction, DIplus, DIminus, upper, lower, ema50_r = self.indicators_signal(pair)

        if None in em50:
            print("no_moves", flush=True)
            return

        current_price = self.data[pair]['close'][-1]
        can_buy = buy_stack / current_price / 1

        # Block all other signals if a trade is open
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
