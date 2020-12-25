from decimal import Decimal

import numpy as np
import pandas as pd

from agent.strategy.movingaverage import StrategyMovingAverage, \
    EnvelopedAverage, Average, ExponentialAverage
from agent.strategy.strategy import BUY, SELL, NONE


def load_file():
    return pd.read_csv(
        '../../source/BTC-USD_5Y_prev20_aft1.csv',
        names=['Date', 'Open', 'High', 'Low',
               'Close',
               'Adj Close', 'Volume'],
        header=0,
        float_precision=5,
        decimal=','
    )


def expected_output():
    df = load_file()

    y = []
    source = []
    past_values = []

    PREVIOUS_DAYS_COUNT = 20

    last_index = len(df) - 1

    for i, data in df.iterrows():
        source.append(data)

    for i, data in enumerate(source):
        current_value = data['Close']
        past_values.append(Decimal(current_value))
        if PREVIOUS_DAYS_COUNT < i < last_index:
            next_value = source[i + 1]['Close']
            if next_value > current_value:
                signal = BUY
            elif current_value > next_value:
                signal = SELL
            else:
                signal = NONE

            y.append(signal)
    return np.array(y)


def close_values_data():
    df = load_file()

    x = []
    source = []
    past_values = []

    PREVIOUS_DAYS_COUNT = 20

    last_index = len(df) - 1

    for i, data in df.iterrows():
        source.append(data)

    for i, data in enumerate(source):
        current_value = data['Close']
        past_values.append(Decimal(current_value))
        if PREVIOUS_DAYS_COUNT < i < last_index:
            row = np.array([data['Open']] + past_values[-PREVIOUS_DAYS_COUNT:])

            x.append(row)
    return np.array(x)


def get_all_strategies():
    return [
        StrategyMovingAverage([Average(14)]),
        StrategyMovingAverage([Average(20)]),
        StrategyMovingAverage([EnvelopedAverage(14, 0.03)]),
        StrategyMovingAverage([EnvelopedAverage(14, 0.05)]),
        StrategyMovingAverage([EnvelopedAverage(20, 0.03)]),
        StrategyMovingAverage([EnvelopedAverage(20, 0.05)]),
        StrategyMovingAverage([Average(7), Average(14)]),
        StrategyMovingAverage([Average(5), Average(20)]),
        StrategyMovingAverage([Average(4), Average(9), Average(18)]),
        StrategyMovingAverage([ExponentialAverage(7)]),
        StrategyMovingAverage([ExponentialAverage(14)]),
        StrategyMovingAverage([ExponentialAverage(20)]),
    ]


def get_mean_strategies():
    return [
        StrategyMovingAverage([Average(20)]),
        StrategyMovingAverage([EnvelopedAverage(14, 0.03)]),
        StrategyMovingAverage([Average(5), Average(20)]),
        StrategyMovingAverage([Average(4), Average(9), Average(18)]),
        StrategyMovingAverage([ExponentialAverage(7)]),
        StrategyMovingAverage([ExponentialAverage(20)]),
    ]


def get_lastyear_strategies():
    return [
        StrategyMovingAverage([Average(14)]),
        StrategyMovingAverage([Average(20)]),
        StrategyMovingAverage([EnvelopedAverage(14, 0.05)]),
        StrategyMovingAverage([EnvelopedAverage(20, 0.03)]),
        StrategyMovingAverage([EnvelopedAverage(20, 0.05)]),
        StrategyMovingAverage([ExponentialAverage(7)]),
    ]

def get_strategies():
    return get_all_strategies()

def strategy_based_data():
    df = load_file()

    x = []
    source = []
    past_values = []
    strategies = get_strategies()

    PREVIOUS_DAYS_COUNT = 20

    last_index = len(df) - 1

    for i, data in df.iterrows():
        source.append(data)

    for i, data in enumerate(source):
        current_value = data['Close']
        past_values.append(Decimal(current_value))
        if PREVIOUS_DAYS_COUNT < i < last_index:

            row = []

            for s in strategies:
                row.append(s.get_signal(past_values=past_values,
                                        current_value=Decimal(current_value)))

            x.append(row)
    return np.array(x)
