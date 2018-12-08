import json
import numpy as np
import pandas
import re

from dsi.common.quandl_data import QuandlDataSource
from dsi.common.single_asset_portoflio import Portfolio, SingleAssetPortfolio
from dsi.common.config.strategy_config import StrategyConfig
from dsi.common.config.input_config import InputConfig

class SessionConfig:
    def __init__(self):
        self.config = {}
        self._strategies = []
        self._input = None

    @property
    def strategies(self):
        if not self._strategies:
            self._strategies = [StrategyConfig(c) for c in self.config.get('strategies', [])]
        return self._strategies

    @property
    def input(self):
        if not self._input:
            self._input = InputConfig(self.config['input'])
        return self._input

    def load_file(self, file):
        with open(file) as config_file:
            config_content = config_file.read()
            self.load_json(config_content)

    def load_json(self, json_string):
        self.config = json.loads(json_string)

    def get_initial_portfolio(self):
        if 'single_asset_portfolio' in self.config:
            return SingleAssetPortfolio(
                initial_currency=self.config['single_asset_portfolio']['initial_currency'], initial_asset=self.config['single_asset_portfolio']['initial_asset'])
        elif 'portfolio' in self.config:
            portfolio = Portfolio()
            for s in self.config['portfolio']:
                portfolio.add_security(s, self.config['portfolio'][s])
            return portfolio
        else:
            raise "No valid portfolio has been found in the config"
