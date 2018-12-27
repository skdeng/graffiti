from .limit_order_book import LimitOrderBook


class MarketFrame:
    def __init__(self, timestamp: str):
        self.timestamp = timestamp
        self.prices = {}
        self.orderbook = {}
        self.split_ratio = {}

    def add_ticker(self, ticker: str, o: float, c: float, h: float, l: float, adj_o: float, adj_c: float, adj_h: float, adj_l: float, split_ratio: float):
        self.prices[ticker] = PriceCandle(
            o, c, h, l, adj_o, adj_c, adj_h, adj_l)
        if split_ratio > 1.0:
            self.split_ratio[ticker] = split_ratio

    def add_ticker_from_datarow(self, datarow):
        self.prices[datarow['ticker']] = PriceCandle(datarow['open'], datarow['close'], datarow['high'], datarow['low'],
                                                     datarow['adj_open'], datarow['adj_close'], datarow['adj_high'], datarow['adj_close'])
        if datarow['split_ratio'] > 1.0:
            self.split_ratio[datarow['ticker']] = datarow['split_ratio']


class PriceCandle:
    def __init__(self, o: float, c: float, h: float, l: float, adj_o: float, adj_c: float, adj_h: float, adj_l: float):
        self.o = o
        self.c = c
        self.h = h
        self.l = l

        self.adj_o = adj_o
        self.adj_c = adj_c
        self.adj_h = adj_h
        self.adj_l = adj_l
