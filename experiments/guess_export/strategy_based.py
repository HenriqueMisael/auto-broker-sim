from decimal import Decimal

import pandas as pd

from agent.strategy.movingaverage import StrategyMovingAverage, \
    ExponentialAverage, Average, EnvelopedAverage

stock_history = pd.read_csv(
    '../../source/BTC-USD_5Y_prev20_aft1.csv',
    names=['Date', 'Open', 'High', 'Low',
           'Close',
           'Adj Close', 'Volume'],
    header=0,
    float_precision=5,
    decimal=','
)

output = []
source = []
past_values = []
strategies = [
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

PREVIOUS_DAYS_COUNT = 20

last_index = len(stock_history) - 1

for i, data in stock_history.iterrows():
    source.append(data)

for i, data in enumerate(source):
    current_value = data['Close']
    past_values.append(Decimal(current_value))
    if PREVIOUS_DAYS_COUNT < i < last_index:

        row = []

        for s in strategies:
            row.append(s.get_signal(past_values=past_values,
                                    current_value=Decimal(current_value)))

        next_value = source[i + 1]['Close']

        signal = 'HOLD'
        if next_value > current_value:
            signal = 'BUY'
        elif current_value > next_value:
            signal = 'SELL'

        row.append(signal)

        output.append(row)

pd.DataFrame(output,
             columns=list(s.__str__() for s in strategies) + [
                 'expected_signal',
             ]).to_csv('../../output/guess_export.csv', index=False,
                       line_terminator='\n')
