# Orders

3 types of orders are currently supported: Limit order, Market order and Stop order. They are available in the `graffiti.market` module.

## Market order

Market orders are executed at the open price of the next market frame.

    order = MarketOrder(base_currenc="USD", ticker="MSFT", volume=2, order_side=OrderSide.Buy)

Note that `order_side` must be `OrderSide.Buy` or `OrderSide.Sell`, which can be imported from the `graffiti.market` module

### Simplified market order

Market order can be simplified as a tuple in the following format, with positive volume for buy orders and negative volume for sell orders

    (base_currency, stock_symbol, volume)

Base currency and stock symbol can be omitted. If base_currency is omitted, the [default currency](./market.md#Default_Currency) is used. If both base_currency and stock_symbol are omitted, the [default](./market.md#Default_Asset) with be used for both. The following are all valid orders

    ("USD", "MSFT", 1)
    ("MSFT", -2)
    (0)
    -5

## Limit order

Limit orders are added to the list of active orders and are processed for every time frame. For each time frame and each order, if the open price is more advantageous than the limit price of the order (lower for buy order, higher for sell order), the order is executed at open price. Otherwise, if the limit price is comprise within the high-low range, it is executed at the limit price.

    order = LimitOrder(base_currency="USD", ticker="MSFT", volume=2, order_side=OrderSide.Sell, limit_price=50)

## Stop order

Missing doc