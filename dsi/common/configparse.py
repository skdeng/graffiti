import numpy as np
import pandas

from dsi.common.quandl_data import QuandlDataSource
from dsi.common.single_asset_portoflio import Portfolio, SingleAssetPortfolio


def get_portfolio(config):
    if 'single_asset_portfolio' in config:
        return SingleAssetPortfolio(
            initial_currency=config['single_asset_portfolio']['initial_currency'], initial_asset=config['single_asset_portfolio']['initial_asset'])
    elif 'portfolio' in config:
        portfolio = Portfolio()
        for s in config['portfolio']:
            portfolio.add_security(s, config['portfolio'][s])
        return portfolio
    else:
        raise "No valid portfolio has been found in the config"


def get_inputpricedata(config):
    if 'input' in config:
        config_input = config['input']
        input_type = config_input['type']
        if input_type == 'file':
            return pandas.read_csv(config['file'])
        elif input_type == 'quandl':
            quandl_data_source = QuandlDataSource(config_input['api_key'])
            return np.array(quandl_data_source.get_us_stock_daily_close(config_input['symbol'])['close'])
    else:
        raise "Config does not have an input section"
