import matplotlib.pyplot as plt
import numpy as np

from dsi.common.quandl_data import QuandlDataSource
from dsi.data_processor.data_filter import conv_smoothing
from dsi.data_processor.data_label import (get_buysell_points_coordinates,
                                           get_local_buysell_label)

data_source = QuandlDataSource('xM6Bh-vY7JsUncDqo7SE')
msft_data = data_source.get_us_stock_daily('MSFT')

price = np.array(msft_data['close'])
plt.plot(price)

smoothed_price = conv_smoothing(price, window_len=15)
plt.plot(smoothed_price)

buy_sell_label = get_local_buysell_label(smoothed_price)
buy_x, buy_y, sell_x, sell_y = get_buysell_points_coordinates(
    smoothed_price, buy_sell_label)

plt.scatter(buy_x, buy_y, c='green', s=10, marker='x')
plt.scatter(sell_x, sell_y, c='red', s=10, marker='o')

plt.show()
