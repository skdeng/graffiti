from .order import Order, OrderSide


class Trade:
    def __init__(self, timestamp: str, base_currency: str, ticker: str,
                 volume: float, price: float,
                 side: OrderSide):
        self.base_currency = base_currency
        self.ticker = ticker
        self.volume = volume
        self.price = price
        self.side = side

    @classmethod
    def from_order(cls, timestamp: str, order: Order, executed_price: float, executed_volume: float):
        return cls(timestamp, order.base_currency, order.ticker, executed_volume, executed_price, order.order_side)

    def __str__(self):
        return "{} {}{} {} at {}".format(self.side.name, self.ticker, self.base_currency, self.volume, self.price)
