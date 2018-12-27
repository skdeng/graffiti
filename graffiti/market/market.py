import logging
from copy import deepcopy
from math import isclose
from time import time
from typing import Iterable, List, Mapping

from pandas import DataFrame

from graffiti.common.functions import select_sum

from .market_frame import MarketFrame
from .order import Order, OrderSide
from .portfolio import Portfolio
from .trade import Trade


class Market:
    def __init__(self, initial_portfolio: Portfolio, flat_fee: float, ratio_fee: float, base_currency='USD'):
        self.active_orders = set()
        self.market_frames = {}
        self.time_frames = []
        self.current_market_frame_index = 0
        self.portfolio: Portfolio = deepcopy(initial_portfolio)
        self.initial_portfolio: Portfolio = initial_portfolio
        self.trades = []
        self.flat_fee = flat_fee
        self.ratio_fee = ratio_fee
        self.base_currency = base_currency

        self.portfolio_value_history = []

    @property
    def current_market_frame(self) -> MarketFrame:
        return self.market_frames[self.time_frames[self.current_market_frame_index]]

    @property
    def execution_completion(self) -> float:
        return self.current_market_frame_index / len(self.market_frames)

    def step(self, orders: Iterable[Order], delay: int = 0):
        """
        Move to the next timeframe and process open orders

        Args:
            orders (Set[Order]): New orders to place
            delay (int, optional): Defaults to 0. Minimum delay to the next timeframe. 0 means the next closest available time frame
        """

        self.active_orders = self.active_orders.union(orders)
        self._process_open_orders()

        for asset in self.portfolio.securities:
            if asset in self.current_market_frame.split_ratio and self.current_market_frame.split_ratio[asset] > 1.0:
                self.portfolio[asset] *= self.current_market_frame.split_ratio[asset]

        self.portfolio_value_history.append(self.get_current_portfolio_value())
        return self._step_market_frame()

    def reset(self):
        self.active_orders = set()
        self.portfolio = deepcopy(self.initial_portfolio)
        self.trades = []
        self.current_market_frame_index = 0
        self.portfolio_value_history = []

    def open_order(self, order: Order):
        pass

    def cancel_order(self, order: Order):
        pass

    def get_buy_vwap(self, base_currency=Portfolio.default_currency, ticker=Portfolio.default_asset) -> float:
        trades = list(filter(lambda t: (t.ticker ==
                                        ticker and t.side == OrderSide.Buy), self.trades))
        return select_sum(lambda t: t.volume * t.price, trades) / select_sum(lambda t: t.volume, trades)

    def get_sell_vwap(self, base_currency=Portfolio.default_currency, ticker=Portfolio.default_asset) -> float:
        trades = list(filter(lambda t: (t.ticker ==
                                        ticker and t.side == OrderSide.Sell), self.trades))
        return select_sum(lambda t: t.volume * t.price, trades) / select_sum(lambda t: t.volume, trades)

    def get_vwap(self, base_currency=Portfolio.default_currency, ticker=Portfolio.default_asset) -> (float, float):
        return self.get_buy_vwap(base_currency, ticker), self.get_sell_vwap(base_currency, ticker)

    def apply_all_orders(self, orders: List[Iterable[Order]], step_callback=None):
        assert len(orders) == len(self.market_frames), "order length: {}, number of market frames: {}".format(
            len(orders), len(self.market_frames))
        for current_orders in orders:
            self.step(current_orders)
            if step_callback:
                step_callback(self)

    def add_price_data(self, price_data: DataFrame):
        for _, row in price_data.iterrows():
            if row['date'] not in self.market_frames:
                self.market_frames[row['date']] = MarketFrame(row['date'])
            self.market_frames[row['date']].add_ticker_from_datarow(row)

        self.time_frames += price_data['date'].tolist()

        self.time_frames = list(set(self.time_frames))
        self.time_frames.sort()

        if len(price_data['ticker'].unique()) == 1:
            Portfolio.default_asset = price_data['ticker'][0]

    def get_current_portfolio_value(self):
        value = 0
        for symbol, amount in self.portfolio.securities.items():
            if symbol == self.base_currency:
                value += amount
            else:
                value += amount * self.current_market_frame.prices[symbol].c
        return value

    def _process_open_orders(self):
        order_for_deletion = set()
        for order in self.active_orders:
            execution_price, execution_volume = order.get_trade(
                self.current_market_frame)
            if execution_volume > 0:
                self._buy_asset(order.base_currency, order.ticker, execution_volume, execution_price) if order.order_side == OrderSide.Buy else self._sell_asset(
                    order.base_currency, order.ticker, execution_volume, execution_price)
                executed_trade = Trade.from_order(timestamp=self.time_frames[self.current_market_frame_index],
                                                  order=order, executed_price=execution_price, executed_volume=execution_volume)
                self.trades.append(executed_trade)
                order_for_deletion.add(order)
        self.active_orders = self.active_orders - order_for_deletion

    def _buy_asset(self, base_currency: str, asset: str, volume: float, price: float):
        total_price = volume * price
        total_price = total_price * (1 + self.ratio_fee) + self.flat_fee

        # todo prevent overdraw

        self.portfolio.add_security(base_currency, -total_price)
        self.portfolio.add_security(asset, volume)

    def _sell_asset(self, base_currency: str, asset: str, volume: float, price: float):
        # todo prevent overdraw

        total_price = volume * price
        total_price = total_price / (1 + self.ratio_fee) - self.flat_fee

        self.portfolio.add_security(base_currency, total_price)
        self.portfolio.add_security(asset, -volume)

    def _step_market_frame(self):
        self.current_market_frame_index += 1
        if self.current_market_frame_index >= len(self.market_frames):
            return False
        else:
            return True
