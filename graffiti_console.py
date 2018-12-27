import argparse
import importlib.util
import inspect
import json
import logging
import ntpath
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from graffiti.common.config import SessionConfig
from graffiti.market import Market, MarketFrame, Order, convert_simple_order


def init_logging(log_level: str):
    log_level = getattr(logging, log_level)
    logging.basicConfig(level=log_level)
    log_formatter = logging.Formatter(
        "[%(levelname)s] [%(name)s] %(message)s")
    for h in logging.getLogger().handlers:
        h.setFormatter(log_formatter)


def market_step_callback(market: Market):
    print("Strategy completion: {}%".format(
        int(market.execution_completion * 100)), end='\r')
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='graffiti runner')
    parser.add_argument('-c', '--config', type=str,
                        help='Config file for the strategy')
    parser.add_argument('--log', type=str, default='INFO',
                        help='Logging level. Possible values: DEBUG, INFO, WARNING, ERROR, CRITICAL')

    args = parser.parse_args()

    init_logging(args.log.upper())
    logging.info("Initializing...")

    config = SessionConfig()
    if args.config is None:
        args.config = 'C:\\Users\\deng_\\OneDrive\\Code\\graffiti\\config\\baseconfig.json'
        # print("Please provide a config file...")
        # exit()

    config.load_file(args.config)

    price_data = config.input.get_data()

    legend_titles = []

    for strategy_config in config.strategies:
        if strategy_config.enabled:
            logging.info("Starting strategy " + strategy_config.name)

            portfolio = strategy_config.get_initial_portfolio()
            market = Market(portfolio, strategy_config.flat_fee,
                            strategy_config.ratio_fee)
            market.add_price_data(price_data)

            strategy_instance = strategy_config.get_strategy_instance()
            if strategy_instance:
                while True:
                    orders = strategy_instance.step(
                        market.current_market_frame, market.portfolio)
                    orders = convert_simple_order(orders)
                    if not market.step(orders):
                        break
                    market_step_callback(market)
            else:
                strategy_function = strategy_config.get_strategy_function()
                trade_actions = strategy_function(
                    price_data, strategy_config.config)

                orders = [convert_simple_order(
                    actions) for actions in trade_actions]
                market.apply_all_orders(orders, market_step_callback)

            portfolio_history = market.portfolio_value_history
            pl_history = list(
                map(lambda p: p/portfolio_history[0], portfolio_history))
            plt.plot(pl_history)
            final_pl = 100*(pl_history[-1] - 1)
            legend_titles.append("{} final PL: {}%".format(
                strategy_config.name, int(final_pl)))

            logging.info("Finish strategy " + strategy_config.name)

    input_display = config.input.display
    if input_display:
        price_data_close = price_data['adj_close'] if input_display == 'adjusted' else price_data['close']
        price_data_change = price_data_close / price_data_close[0]
        plt.plot(price_data_change)
        legend_titles.append('Price')

    legend_titles = tuple(legend_titles)
    plt.legend(legend_titles)
    plt.show()
