# Configuration files

Configuration files are used to run this app. There are 3 major sections in a configuration file:

- `input`
- `strategies`
- `portfolio`

## Input data

Input data is defined within the `input` element of the config. It requires 4 parameters:

| Name | Description | Note |
| --- | --- | --- |
| `input_type` | Type of the input. Currently supported values are `file` or `quandl` | |
| `input_source` | Input source for the input type. File path for `file` input and API key for `quandl` input | Can retrieve values from environment variables by prepending `env:` to the variable name. E.g.: `env:quandl_api_key` |
| `symbol` | Trade symbol for input data | Letter casing does not matter |
| `display` | Whether the price data will be plotted and how it will be shown. Can be set to `true`, `false` or `"adjusted"`. | If set to `"adjusted"`, the price data will be normalized based on splits |

## Strategies

Each strategies is defined as an element in the `strategies` array. All parameters below except `file` are optional.

| Name | Description | Default value |
|---|---|---|
| `file` | Path to the strategy file |  |
| `name` | Name of the strategy | \<Name of the strategy file\> |
| `enabled` | Strategies that are marked as `enabled: false` won't be run | `true` |
| `flat_fee` | Flat fee on every transaction in base currency | `0` |
| `ratio_fee` | Percent fee on every transaction in base currency | `0` |
| `config` | Custom configuration object that can be access from the strategy | `{}` |
| `portfolio` | A startegy-specific portfolio can be defined, which will override the global portfolio | \<Global portfolio\> |

## Portfolio

A global portfolio is defined under the `portfolio` element, with each asset in the portfolio defined as a key-value pair.