import numpy as np

from graffiti.common.functions import select_sum
from . import OrderSide
from . import Trade
from . import Portfolio


class SingleAssetPortfolio(Portfolio):
    def __init__(self, currency_symbol=Portfolio.default_currency, asset_symbol=Portfolio.default_asset, initial_currency=0, initial_asset=0, overdraw=False):
        """
        Constructor
            :param self: self
            :param currency_symbol: Symbol of the currency
            :param asset_symbol: Symbol of the asset
            :param initial_currency=0: Starting currency amount
            :param initial_asset=0: Starting asset amount
            :param overdraw=False: Whether trade actions that result in negative currency/asset amounts are allowed
        """
        super().__init__(overdraw=overdraw)
        self.currency = currency_symbol
        self.asset = asset_symbol
        self.securities[self.currency] = initial_currency
        self.securities[self.asset] = initial_asset
        self.orders = []

    def get_currency(self):
        return self.securities[self.currency]

    def get_asset(self):
        return self.securities[self.asset]

    def buy(self, amount, price, flat_fee=0, ratio_fee=0):
        total_price = amount * price
        total_price = total_price * (1 + ratio_fee) + flat_fee

        if not self.overdraw and total_price > self.get_currency():
            return 0

        self.add_security(self.currency, -total_price)
        self.add_security(self.asset, amount)

        self.orders.append(Trade(base_currency=self.currency, ticker=self.asset,
                                volume=amount, price=price,
                                side=OrderSide.Buy))
        return amount

    def sell(self, amount, price, flat_fee=0, ratio_fee=0):
        if not self.overdraw and amount > self.get_asset():
            return 0

        total_price = amount * price
        total_price = total_price / (1 + ratio_fee) - flat_fee

        self.add_security(self.currency, total_price)
        self.add_security(self.asset, -amount)

        self.orders.append(Trade(base_currency=self.currency, ticker=self.asset,
                                volume=amount, price=price,
                                side=OrderSide.Sell))
        return amount

    def total_buyable_amount(self, price, flat_fee=0, ratio_fee=0):
        total_currency = self.get_currency()
        usable_currency = (total_currency - flat_fee) / (1 + ratio_fee)
        return usable_currency / price

    def get_total_value(self, price):
        return self.get_currency() + self.get_asset() * price

    def apply_trade_actions(self, price_series, trade_actions, flat_fee=0, ratio_fee=0):
        price_series_close = price_series['close']
        assert len(trade_actions) == len(price_series)
        history = []
        history.append(self.get_total_value(price_series_close[0]))
        for i in range(len(trade_actions)):
            trade_volume = abs(trade_actions[i])
            if trade_actions[i] > 0:
                self.buy(
                    amount=trade_volume, price=price_series_close[i], flat_fee=flat_fee, ratio_fee=ratio_fee)
            elif trade_actions[i] < 0:
                self.sell(
                    amount=trade_volume, price=price_series_close[i], flat_fee=flat_fee, ratio_fee=ratio_fee)

            if price_series['split_ratio'][i] > 1.0:
                self.securities[self.asset] *= price_series['split_ratio'][i]
            history.append(self.get_total_value(price_series_close[i]))

        return np.round(history, decimals=2)

    def get_orders_vwap(self):
        buy_orders = list(filter(lambda o: o.side == OrderSide.Buy, self.orders))
        buy_vwap = select_sum(lambda o: o.volume * o.price,
                              buy_orders) / select_sum(lambda o: o.volume, buy_orders)

        sell_orders = list(filter(lambda o: o.side == OrderSide.Sell, self.orders))
        sell_vwap = select_sum(lambda o: o.volume * o.price, sell_orders) / \
            select_sum(lambda o: o.volume, sell_orders)

        return buy_vwap, sell_vwap
