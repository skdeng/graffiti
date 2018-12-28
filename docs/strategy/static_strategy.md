# Static Strategy

A static strategy is a trade strategy that depends only the market price at each point in time. Such strategies are not very flexible and are not recommended beyond initial experimentations. See [Dynamic Strategy](./dynamic_strategy.md) for a more flexible implementation.

## Structure

A static strategy is defined as a single python script with a `run_strategy` function as entry point. `run_strategy` must accept 2 arguments: `price_data` and `config`.

### Arguments

**price_data**: an ordered list of [market frames](../market/market_frame.md). This contains all available price data read from the inputs.

**config**: the configuration element under the [strategy](../config_files.md#Strategies) in the [configuration file](../config_files.md). This is un-processed and can be used to configure the strategy on-the-fly without modification to the code.

### Return value

The function should return an iterable collection of [orders](../market/orders.md) for each timeframe, aggregated into a list. Therefore, the returned list needs to be the same length as the input list of price data.