from random import randint

import numpy as np
import pandas as pd

from graffiti.common.quandl_data import QuandlDataSource
from graffiti.market import Market, MarketOrder, OrderSide, Portfolio


def get_test_market():
    portfolio = Portfolio()
    initial_usd = 100000
    initial_stock = 100
    portfolio.add_security("USD", initial_usd)
    portfolio.add_security("MSFT", initial_stock)

    price_data = pd.read_csv('test/testdata/msft_daily.csv')

    market = Market(portfolio, 0, 0)
    market.add_price_data(price_data)
    return initial_usd, initial_stock, price_data, market


def test_market_step_market_orders():
    initial_usd, initial_stock, price_data, market = get_test_market()

    order_sides = [OrderSide.Buy, OrderSide.Sell]
    for order_side in order_sides:
        prev_usd = initial_usd
        prev_stock = initial_stock
        for i in range(0, 10):
            order_size = randint(1, 6)
            current_open_price = price_data['open'][i]
            order = MarketOrder("USD", "MSFT", order_size, order_side)

            market.step([order])

            m = 1 if order_side == OrderSide.Buy else -1

            assert market.portfolio["USD"] == prev_usd - \
                order_size * current_open_price * m
            assert market.portfolio["MSFT"] == prev_stock + order_size * m
            assert market.trades[-1].price == current_open_price
            assert market.trades[-1].volume == order_size

            prev_usd = market.portfolio["USD"]
            prev_stock = market.portfolio["MSFT"]
        market.reset()


def test_market_applyall_market_orders():
    initial_usd, initial_stock, price_data, market = get_test_market()

    # 1 order per time frame
    volume = [randint(-5, 5) for i in range(len(price_data))]
    market_orders = [[MarketOrder("USD", "MSFT", abs(
        v), OrderSide.Buy if v > 0 else OrderSide.Sell)] for v in volume]
    market.apply_all_orders(market_orders)

    currency_volume = price_data['open'] * volume

    assert market.portfolio["USD"] == initial_usd - sum(currency_volume)
    assert market.portfolio["MSFT"] == initial_stock + sum(volume)
