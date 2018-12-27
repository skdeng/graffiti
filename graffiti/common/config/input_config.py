import logging
import os

import pandas as pd

from graffiti.common.quandl_data import QuandlDataSource


class InputConfig:
    def __init__(self, config_root):
        self.config_root = config_root

    @property
    def input_type(self) -> str:
        return self.config_root['input_type']

    @property
    def input_source(self) -> str:
        src = self.config_root['input_source']
        if src.startswith("env:"):
            envvar = src.split("env:", 1)[1]
            return os.environ[envvar]
        else:
            return self.config_root['input_source']

    @property
    def symbol(self) -> str:
        return self.config_root['symbol']

    @property
    def display(self) -> str:
        return self.config_root.get('display', False)

    def get_data(self):
        logging.debug("Loading price data from {}".format(self.input_type))
        if self.input_type == 'quandl':
            quandl_data_source = QuandlDataSource(self.input_source)
            return quandl_data_source.get_us_stock_daily(self.symbol)
        elif self.input_type == 'file':
            return pd.read_csv(self.input_source)
        else:
            raise "Unknown input type " + self.input_type
