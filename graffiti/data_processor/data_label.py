import numpy as np
from scipy.signal import argrelextrema


def get_local_buysell_label(price_series, price_diff_min=0, hold_label=0, buy_label=1, sell_label=-1):
    """
    Calculate buy sell labels of a price series using local extrema
        :param price_series: Prices series
        :param price_diff_min=0: Minimum difference between 2 extrema to be considered
        :param hold_label=0: Label for no action
        :param buy_label=1: Label for buy action
        :param sell_label=-1: Label for sell action
    """
    local_max = argrelextrema(price_series, np.greater)[0]
    local_min = argrelextrema(price_series, np.less)[0]

    if local_max[0] > local_min[0]:
        local_min = np.insert(local_min, 0, 0)
    else:
        local_max = np.insert(local_max, 0, 0)

    local_ex = np.concatenate((local_max, local_min))
    local_ex.sort()

    buy_points = []
    sell_points = []

    for i in range(1, len(local_ex)):
        index = local_ex[i]
        is_max = True if index in local_max else False
        diff = abs(price_series[index] - price_series[local_ex[i-1]])

        if diff >= price_diff_min:
            if is_max:
                sell_points.append(index)
            else:
                buy_points.append(index)
        else:
            # if the difference is smaller than price_diff_min, skip the current point, and also remove the previous point
            if is_max:
                del buy_points[-1]
            else:
                del sell_points[-1]

    all_points = np.zeros_like(price_series, dtype=int)
    all_points += hold_label
    all_points[buy_points] = buy_label
    all_points[sell_points] = sell_label

    return all_points


def get_buysell_points_coordinates(price_series, labels, buy_label=1, sell_label=-1):
    """
    Given a price series and labels for each price point, generate the x and y coordinates for the buy sell points to display on graph
        :param price_series: input price series
        :param labels: buy sell labels
        :param buy_label=1: buy label
        :param sell_label=-1: sell label
    """
    buy_x = []
    buy_y = []
    sell_x = []
    sell_y = []
    for i in range(len(labels)):
        if labels[i] == buy_label:
            buy_x.append(i)
            buy_y.append(price_series[i])
        elif labels[i] == sell_label:
            sell_x.append(i)
            sell_y.append(price_series[i])
    return buy_x, buy_y, sell_x, sell_y


def get_price_change_label(price_series, type='ratio'):
    """
    Calculate the price change between each time frame given a price series
        :param price_series: Prices series
        :param type='ratio': Possible values ''
    """
    price_series_base = price_series[:-1]
    price_series_forward = price_series[1:]

    if type == 'ratio':
        return price_series_forward / price_series_base
    elif type == 'value':
        return price_series_forward - price_series_base
