import numpy as np
from scipy.signal import argrelextrema


def get_local_buysell_label(price_series, price_diff_min=0, hold=0, buy_label=1, sell_label=-1):
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

        if diff > price_diff_min:
            if is_max:
                sell_points.append(index)
            else:
                buy_points.append(index)

    all_points = np.zeros_like(price_series, dtype=int)
    all_points[buy_points] = buy_label
    all_points[sell_points] = sell_label

    return all_points
