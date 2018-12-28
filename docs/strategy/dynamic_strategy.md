# Dyanmic Strategy

A dynamic strategy is a strategy that changes factors other than the market price, such as the quantity of each asset held.

## Structure

A dynamic strategy is defined as a class that ends with the word **strategy** (casing does not matter). _Note that if there are multiple class defined with the suffix **strategy**, the runner will throw an error._

The constructor must accept a single argument `config` which will contains the [configuration element in the configuration file](../config_files.md#Strategies).

## Step 

The class must have a method called `step` with 2 arguments. The strategy should not modify any of the inputs that are passed in.

**current_market_frame**: Market frame for the current time.

**current_portfolio**: state of the portfolio for the current time.

The step function should return an iterable collection of [orders](../market/orders.md) to apply. Iterable collection can be `list`, `set`, `tuple`, or other types that can be iterated over with a `for` loop.

    [order1, order2, order3]        # list
    (order1, order2, order3)        # tuple
    set({order1, order2, order3})   # set