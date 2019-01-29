# Project Graffiti

[![Build Status](https://travis-ci.com/skdeng/graffiti.svg?branch=master)](https://travis-ci.com/skdeng/graffiti)

Project Graffiti is a framework for testing algorithmic trading strategies. It handles all the extra overhead so that you can focus on designing the best strategy to beat the market. This is essentially the python implementation of [Project Black Cross](https://github.com/skdeng/blackcross)

## Getting Started

The latest version of Python 3 is needed. See [official Python website](https://www.python.org/downloads/release/python-371/) for instruction.

Install python packges:

`pip install --user -r requirements.txt`

## How to run

### Using the console runner

`python graffiti_console.py -c <path to configuration file>`

For more details on configuration files, see [Configuration Files](./docs/config_files.md)

### GUI

Coming soon

## Development

[How to create new trade strategies](./docs/strategy/static_strategy.md)
