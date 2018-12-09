import argparse
import importlib.util
import json
import ntpath
import os

import matplotlib.pyplot as plt
import numpy as np

from dsi.common.config.session_config import SessionConfig

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='DSI runner')
    parser.add_argument('-c', '--config', type=str,
                        help='Config file for the strategy')
    parser.add_argument('-p', '--param', type=str, nargs='*',
                        help='Additional config parameters. This will overwrite existing parameters in the config file')

    args = parser.parse_args()

    # get a portfolio
    config = SessionConfig()
    config.load_file(args.config)

    price_data = config.input.get_data()
    
    legend_titles = []

    for strategy_config in config.strategies:
        if strategy_config.enabled:
            # import from the strategy file
            strategy_spec = importlib.util.spec_from_file_location(
                'module.name', strategy_config.file)
            strategy_module = importlib.util.module_from_spec(strategy_spec)
            strategy_spec.loader.exec_module(strategy_module)
            strategy_function = strategy_module.run_strategy

            legend_titles.append(strategy_config.name)

            portfolio = config.get_initial_portfolio()
            trade_actions = strategy_function(
                price_data, strategy_config.config)

            flat_fee = strategy_config.flat_fee
            ratio_fee = strategy_config.ratio_fee

            portfolio_history = portfolio.apply_trade_actions(
                price_data, trade_actions, flat_fee=flat_fee, ratio_fee=ratio_fee)
            pl_history = portfolio_history / portfolio_history[0]
            plt.plot(pl_history)

    input_display = config.input.display
    if input_display:
        price_data_close = price_data['adj_close'] if input_display == 'adjusted' else price_data['close']
        price_data_change = price_data_close / price_data_close[0]
        plt.plot(price_data_change)
        legend_titles.append('Price')

    legend_titles = tuple(legend_titles)
    plt.legend(legend_titles)
    plt.show()
