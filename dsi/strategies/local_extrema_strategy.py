import numpy as np
from scipy.signal import argrelextrema

from dsi.data_processor.data_label import get_local_buysell_label


def run_strategy(price_data, config):
    return get_local_buysell_label(price_data)
