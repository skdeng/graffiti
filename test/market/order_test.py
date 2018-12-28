from graffiti.market import (MarketOrder, OrderSide, Portfolio,
                             convert_simple_order)


def test_convert_simple_order():
    simple_orders = [1, 2, 0, 3, 1, -5, 0]
    converted_orders = convert_simple_order(simple_orders)

    nonzero_simple_orders = [o for o in simple_orders if o != 0]
    for i in range(len(nonzero_simple_orders)):
        assert converted_orders[i].order_type == "market"
        assert converted_orders[i].volume == abs(nonzero_simple_orders[i])
        assert converted_orders[i].base_currency == Portfolio.default_currency
        assert converted_orders[i].ticker == Portfolio.default_asset
        assert converted_orders[i].order_side == OrderSide.Buy if nonzero_simple_orders[i] > 0 else OrderSide.Sell
