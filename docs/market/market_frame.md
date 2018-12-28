# Market Frame

A market frame is a snapshot of the market at a certain point in time. It is composed of 3 sub-parts: price, orderbook and split ratio. `MarketFrame` class is available in the `graffiti.market` module.

## Price

A market frame has a dictionary of prices for all assets that have available data at that particular time. It can access like so:

    market_frame.prices["asset"]

For each available asset, the snippet above returns a `PriceCandle` object that contains the open, close, high and low price since the previous market_frame for the same asset.

    market_frame.prices["asset"].o # open price
    market_frame.prices["asset"].c # close price
    market_frame.prices["asset"].h # high
    market_frame.prices["asset"].l # low

Split adjusted prices are also available. If there has been no split in the history of the asset, or no split data is available, the adjusted prices are the same as their non-adjusted counterparts.

    market_frame.prices["asset"].adj_o # adjusted open
    market_frame.prices["asset"].adj_c # adjusted close
    market_frame.prices["asset"].adj_h # adjusted high
    market_frame.prices["asset"].adj_l # adjusted low

## Order Book

Currently not available

## Split Ratio

If the stock has gone through a split since the previous market frame. It will have an entry in the `split_ratio` property, and can be retrieve like so

    market_frame.split_ratio["asset"]