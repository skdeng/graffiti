import numpy as np

from graffiti.market import MarketFrame, Portfolio


class ModifiedMeanReversalStrategy:
    def __init__(self, config):
        self.window_length = config['window']
        self.base_currency = config.get(
            'base_currency', Portfolio.default_currency)
        self.ticker = config.get('ticker', Portfolio.default_asset)

        self.epsilon = config.get('epsilon', 0)

        self.window = []

    def step(self, market_frame: MarketFrame, portfolio: Portfolio):
        last_adj_price = market_frame.prices[self.ticker].adj_c
        last_price = market_frame.prices[self.ticker].c
        self.window.append(last_adj_price)

        if len(self.window) < self.window_length:
            return [0]

        if len(self.window) > self.window_length:
            self.window.pop(0)

        ma = np.mean(self.window)
        mstd = np.std(self.window)

        z = -(last_adj_price - ma) / mstd

        current_currency_balance = portfolio[self.base_currency]
        current_asset_balance = portfolio[self.ticker]
        current_total_value = current_currency_balance + \
            current_asset_balance * last_price

        volume = 0

        if z > self.epsilon:
            target_currency_balance = current_total_value / (2+z)
            volume = (current_currency_balance -
                      target_currency_balance) / last_price
        elif z < -self.epsilon:
            target_asset_balance = current_total_value / (2-z)
            volume = target_asset_balance / last_price - current_asset_balance

        return [(self.base_currency, self.ticker, volume)]
