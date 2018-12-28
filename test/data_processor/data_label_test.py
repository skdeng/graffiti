import numpy as np

from graffiti.data_processor.data_label import *


def test_get_local_buysell_label():
    input_data = np.array([1, 2, 6, 4, 5, 6, 7, 3, 2, 1, 7, 3, 5, 2])
    expected_results = np.zeros_like(input_data, dtype=int)
    expected_results[2] = -1
    expected_results[3] = 1
    expected_results[6] = -1
    expected_results[9] = 1
    expected_results[10] = -1
    expected_results[11] = 1
    expected_results[12] = -1
    results = get_local_buysell_label(input_data)
    assert np.array_equal(expected_results, results)


def test_get_local_buysell_label_high_diff_min():
    input_data = np.array([1, 2, 6, 4, 5, 6, 7, 3, 2, 1, 7, 3, 5, 2])
    expected_results = np.zeros_like(input_data, dtype=int)
    expected_results[6] = -1
    expected_results[9] = 1
    expected_results[10] = -1
    results = get_local_buysell_label(input_data, price_diff_min=3)
    assert np.array_equal(expected_results, results)


def test_get_price_change_label():
    input_data = np.array([1, 1, 1])

    expected_results = np.array([1, 1])
    results = get_price_change_label(input_data, type='ratio')
    assert np.array_equal(expected_results, results)

    expected_results = np.array([0, 0])
    results = get_price_change_label(input_data, type='value')
    assert np.array_equal(expected_results, results)

    input_data = np.array([1, 2, 4, 10])
    expected_results = np.array([2, 2, 2.5])
    results = get_price_change_label(input_data, type='ratio')
    assert np.array_equal(expected_results, results)

    expected_results = np.array([1, 2, 6])
    results = get_price_change_label(input_data, type='value')
    assert np.array_equal(expected_results, results)
