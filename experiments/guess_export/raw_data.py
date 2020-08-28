import pandas as pd

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

PREVIOUS_DAYS_COUNT = 20

last_index = len(stock_history) - 1

for i, data in stock_history.iterrows():
    source.append(data)

for i, data in enumerate(source):
    current_value = data['Close']
    past_values.append(current_value)
    if PREVIOUS_DAYS_COUNT < i < last_index:
        row = past_values[-PREVIOUS_DAYS_COUNT:]
        row.append(current_value)
        row.append(data['High'])
        row.append(data['Low'])

        next_value = source[i + 1]['Close']

        signal = 'HOLD'
        if next_value > current_value:
            signal = 'BUY'
        elif current_value > next_value:
            signal = 'SELL'

        row.append(signal)

        output.append(row)

pd.DataFrame(output,
             columns=[
                 '20th_prev_day_close_value',
                 '19th_prev_day_close_value',
                 '18th_prev_day_close_value',
                 '17th_prev_day_close_value',
                 '16th_prev_day_close_value',
                 '15th_prev_day_close_value',
                 '14th_prev_day_close_value',
                 '13th_prev_day_close_value',
                 '12th_prev_day_close_value',
                 '11th_prev_day_close_value',
                 '10th_prev_day_close_value',
                 '09th_prev_day_close_value',
                 '08th_prev_day_close_value',
                 '07th_prev_day_close_value',
                 '06th_prev_day_close_value',
                 '05th_prev_day_close_value',
                 '04th_prev_day_close_value',
                 '03th_prev_day_close_value',
                 '02th_prev_day_close_value',
                 '01th_prev_day_close_value',
                 'current_close',
                 'current_high',
                 'current_low',
                 'expected_signal',
             ]).to_csv('../../output/guess_export.csv', index=False,
                       line_terminator='\n')
