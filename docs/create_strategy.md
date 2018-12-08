# How to create a new trade strategy

## Structure
The entry point must be defined as a `run_strategy(price_data, config)` function inside a python file that takes in `price_data` and `config` as arguments. It must return a list of integers that represent trade volume of the given asset. The list of trade actions has to have the same length as the input price_data. By convention, positive number represent purchase and negative number represent sale.

## Configuration

### Predefined parameters

| Parameter name | Description | Required | Default value |
|---|---|---|---|
| `file` | Path to the strategy file | true |  |
| `name` | Name of the strategy | false | \<Name of the strategy file\> |
| `enabled` | Strategies that are marked as `enabled: false` won't be run | false | true |
| `flat_fee` | Flat fee on every transaction in base currency | false | 0 |
| `ratio_fee` | Percent fee on every transaction in base currency | false | 0 |
| `config` | Custom configuration object that can be access from the strategy | false | empty |

Additional configuration parameters can be passed to the strategy using the `config` parameter. Any sub-items will be passed directly to the strategy