from scipy.signal import argrelextrema
import numpy as np

from graffiti.data_processor.data_filter import *


def test_conv_smoothing():
    """
    Test conv_smoothing
    Method:
    - create a function with a single local extremum
    - add gaussian noise to it to create more local extrema
    - apply smoothing with different window length
    - asser that the smoothed function has less local extrema, and longer window length => less local extrema
    """
    input_data = np.concatenate(
        (np.linspace(0.0, 5.0, num=20), np.linspace(5.0, 0.0, num=20)))
    input_data += np.random.normal(scale=2.0, size=40)
    local_max = argrelextrema(input_data, np.greater)[0]
    local_min = argrelextrema(input_data, np.less)[0]
    extrema_count_before = local_max.size + local_min.size

    smoothed_data = conv_smoothing(input_data, window_len=5)
    local_max = argrelextrema(smoothed_data, np.greater)[0]
    local_min = argrelextrema(smoothed_data, np.less)[0]
    extrema_count_after = local_max.size + local_min.size
    assert extrema_count_after < extrema_count_before

    more_smoothed_data = conv_smoothing(input_data, window_len=10)
    local_max = argrelextrema(more_smoothed_data, np.greater)[0]
    local_min = argrelextrema(more_smoothed_data, np.less)[0]
    extrema_count_final = local_max.size + local_min.size
    assert extrema_count_final < extrema_count_after
