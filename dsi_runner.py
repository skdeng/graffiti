import argparse
import importlib.util
import json
import ntpath
import os

import matplotlib.pyplot as plt
import numpy as np

from dsi.common.configparse import *
from dsi.data_processor.data_filter import *
from dsi.data_processor.data_label import *

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='DSI runner')
    parser.add_argument('-c', '--config', type=str,
                        help='Config file for the strategy')
    parser.add_argument('-p', '--param', type=str, nargs='*',
                        help='Additional config parameters. This will overwrite existing parameters in the config file')

    args = parser.parse_args()

    # get a portfolio
    config = {}
    with open(args.config) as config_file:
        config_content = config_file.read()
        config = json.loads(config_content)

    price_data = get_inputpricedata(config)
    legend_titles = []

    for strategy_config in config['strategies']:
        if not strategy_config.get("enabled", True):
            continue

        # import from the strategy file
        strategy_file = strategy_config['file']
        strategy_spec = importlib.util.spec_from_file_location(
            'module.name', strategy_config['file'])
        strategy_module = importlib.util.module_from_spec(strategy_spec)
        strategy_spec.loader.exec_module(strategy_module)
        strategy_function = strategy_module.run_strategy

        strategy_name = ntpath.basename(strategy_file.rstrip('/\\'))
        strategy_name = os.path.splitext(strategy_name)[0]
        if 'name' in strategy_config:
            strategy_name = strategy_config['name']
        legend_titles.append(strategy_name)

        portfolio = get_portfolio(config)
        trade_actions = strategy_function(
            price_data, strategy_config.get('config', {}))

        flat_fee = strategy_config.get('flat_fee', 0)
        ratio_fee = strategy_config.get('ratio_fee', 0)

        portfolio_history = portfolio.apply_trade_actions(
            price_data, trade_actions, flat_fee=flat_fee, ratio_fee=ratio_fee)
        pl_history = portfolio_history / portfolio_history[0]
        plt.plot(pl_history)

    price_data_change = price_data / price_data[0]
    plt.plot(price_data_change)
    legend_titles.append('Price')
    legend_titles = tuple(legend_titles)
    plt.legend(legend_titles)
    plt.show()
