from enum import Enum
from typing import Iterable, List

from .market_frame import MarketFrame
from .portfolio import Portfolio


class OrderSide(Enum):
    Buy = 0
    Sell = 1


class Order:
    _next_order_number: int = 0

    def __init__(self, order_type: str, base_currency: str, ticker: str, volume: float, order_side: OrderSide):
        self.base_currency = base_currency
        self.ticker = ticker
        self.order_type = order_type
        self.volume = volume
        self.order_side = order_side
        self.order_number: int = Order._next_order_number
        Order._next_order_number += 1

    def get_trade(self, market_frame: MarketFrame):
        pass


class LimitOrder(Order):
    def __init__(self, base_currency: str, ticker: str, volume: float, order_side: OrderSide, limit_price: float):
        super().__init__("limit", base_currency, ticker, volume, order_side)
        self.limit_price = limit_price

    def get_trade(self, market_frame: MarketFrame):
        candle = market_frame[self.ticker]
        if (candle.o <= self.limit_price and self.order_side == OrderSide.Buy) or (candle.o >= self.limit_price and self.order_side == OrderSide.Sell):
            return candle.o, self.volume
        elif (candle.l < self.limit_price and self.order_side == OrderSide.Buy) or (candle.h >= self.limit_price and self.order_side == OrderSide.Sell):
            return self.limit_price, self.volume
        else:
            return 0, 0


class MarketOrder(Order):
    def __init__(self, base_currency: str, ticker: str, volume: float, order_side: OrderSide):
        super().__init__("market", base_currency, ticker, volume, order_side)

    def get_trade(self, market_frame: MarketFrame):
        return market_frame.prices[self.ticker].o, self.volume


class StopOrder(Order):
    def __init__(self, base_currency: str, ticker: str, volume: float, order_side: OrderSide, stop_price: float):
        super().__init__("stop", base_currency, ticker, volume, order_side)
        self.stop_price = stop_price


def convert_simple_order(orders: Iterable) -> List[Order]:
    """
    Convert simple order definitions to Order objects

    Args:
        orders (Iterable): Iterable of simple order definitions. 
        A simple order definition can be in 3 formats: 
            (base_currency, ticker, action)
            (ticker, action)
            action. 
        Action is simply the amount of asset to trade, with positive for buy orderes, and negative for sell orders.

    Returns:
        List[Order]: Set of Order objects
    """

    if orders:
        return_orders = []
        for order in orders:
            order_to_add: Order = None
            if not isinstance(order, Order):
                base_currency = Portfolio.default_currency
                ticker = Portfolio.default_asset
                try:
                    base_currency, ticker, action = order
                except:
                    try:
                        ticker, action = order
                    except:
                        action = order
                if action == 0:
                    continue
                order_to_add = MarketOrder(base_currency, ticker, abs(
                    action), OrderSide.Buy if action > 0 else OrderSide.Sell)
            else:
                order_to_add = order
            if order_to_add.volume != 0:
                return_orders.append(order_to_add)
        return return_orders
