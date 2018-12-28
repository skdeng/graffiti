import json
import logging
import re
from typing import List

import numpy as np
import pandas

from graffiti.common.quandl_data import QuandlDataSource
from graffiti.market import Portfolio, SingleAssetPortfolio

from .input_config import InputConfig
from .strategy_config import StrategyConfig


class SessionConfig:
    def __init__(self):
        self.config = {}
        self._strategies: List[StrategyConfig] = []
        self._input: InputConfig = None

    @property
    def strategies(self) -> List[StrategyConfig]:
        if not self._strategies:
            self._strategies = [StrategyConfig(
                c, self) for c in self.config.get('strategies', [])]
        return self._strategies

    @property
    def input(self) -> InputConfig:
        if not self._input:
            self._input = InputConfig(self.config['input'])
        return self._input

    def load_file(self, file: str):
        logging.debug("Loading configuration from {}".format(file))
        with open(file) as config_file:
            config_content = config_file.read()
            self.load_json(config_content)

    def load_json(self, json_string: str):
        self.config = json.loads(json_string)

    def get_initial_portfolio(self) -> Portfolio:
        if 'portfolio' in self.config:
            return Portfolio.from_config(self.config['portfolio'])
        else:
            raise "No valid portfolio has been found in the config"
