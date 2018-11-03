import numpy as np

from dsi.data_processor.data_label import get_local_buysell_label


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
    result = get_local_buysell_label(input_data)
    assert np.array_equal(expected_results, result)
