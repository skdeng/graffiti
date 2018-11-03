from dsi.data_processor.data_filter import *


def test_moving_average_simple():
    input_data = np.arange(20)
    n = 2
    expected_output = np.arange(19) + 0.5
    output = moving_average(input_data, n)
    assert np.allclose(expected_output, output)

    input_data = np.arange(20)
    n = 3
    expected_output = np.arange(18) + 1
    output = moving_average(input_data, n)
    assert np.allclose(expected_output, output)
