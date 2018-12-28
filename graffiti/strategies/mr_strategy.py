import numpy as np
import pandas as pd


def run_strategy(price_data, config):
    window = config.get("window", 12)
    ticker = config.get('ticker', 'asset')
    price_data_series = price_data['adj_close']

    ma = price_data_series.rolling(window).mean()
    ma = np.nan_to_num(ma)
    stddev = price_data_series.rolling(window).std()
    stddev = np.nan_to_num(stddev)

    zvalue = -(price_data_series - ma) / stddev
    trade_volume = np.copy(zvalue)
    trade_volume[:window] = 0

    trade_volume = [[(ticker, vol)] for vol in trade_volume]

    return trade_volume
