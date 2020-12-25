from decimal import Decimal

import numpy
from sklearn.preprocessing import MinMaxScaler

from agent.machinelearning.ml_agent import MLAgent


class PriceMLAgent(MLAgent):
    scaler: MinMaxScaler

    def __init__(self, name, model, scaler=None,
                 initial_dollar_balance=Decimal(10000)):
        super().__init__(name, model,
                         initial_dollar_balance=initial_dollar_balance)
        self.scaler = scaler
        self.past_inputs = []

    def make_move(self, current_value, open_value=None, high_value=None,
                  low_value=None):
        x = [open_value, high_value, low_value, current_value]
        x = self.scaler.transform([x])[0]
        self.past_inputs.append(x)

        if len(self.past_inputs) < 20:
            return

        past_20_inputs = self.past_inputs[-20:]
        prediction = self.model(numpy.array(past_20_inputs, dtype=float))
        predicted_price = self.scaler.inverse_transform(
            prediction)

        if predicted_price > current_value:
            self.buy_all(current_value)
        elif predicted_price < current_value:
            self.sell_all(current_value)

    def copy(self):
        return PriceMLAgent(self.name, self.model, self.scaler,
                            self.balance_dollar)
