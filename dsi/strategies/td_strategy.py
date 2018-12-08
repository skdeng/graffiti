import numpy as np


def run_strategy(price_data, config):
    immediate_setup_restart = config.get('immediate_setup_restart', True)

    price_data = price_data['close']

    setup_short = [0] * 4
    for i in range(4, len(price_data)):
        current_setup_short = 0
        if price_data[i] > price_data[i-4]:
            if setup_short[-1] == -9:
                current_setup_short = 1 if immediate_setup_restart else 0
            else:
                current_setup_short = setup_short[-1] - 1
        setup_short.append(current_setup_short)

    setup_long = [0] * 4
    for i in range(4, len(price_data)):
        current_setup_long = 0
        if price_data[i] < price_data[i-4]:
            if setup_long[-1] == 9:
                current_setup_long = 1 if immediate_setup_restart else 0
            else:
                current_setup_long = setup_long[-1] + 1
        setup_long.append(current_setup_long)

    setup = np.array([short | long for (short, long)
                      in zip(setup_short, setup_long)])

    trade_actions = np.zeros_like(price_data)
    trade_actions[setup == 9] = 1
    trade_actions[setup == -9] = -1

    return trade_actions
