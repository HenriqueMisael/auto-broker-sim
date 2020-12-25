from decimal import Decimal
from typing import List

import numpy

from agent.strategy.strategy import Strategy


class MLAgent(object):
    balance_btc: Decimal
    balance_dollar: Decimal
    past_values: List[Decimal]
    strategies: List[Strategy]

    net_worth: Decimal
    _last_known_value: Decimal

    def __init__(self, name, model, strategies=None,
                 initial_dollar_balance=Decimal(10000)):
        if strategies is None:
            strategies = []
        self.name = name
        self.balance_btc = Decimal(0)
        self.initial_dollar_balance = initial_dollar_balance
        self.balance_dollar = initial_dollar_balance
        self.past_values = []
        self.strategies = strategies
        self.model = model

    @staticmethod
    def format_money(value):
        return "{:,.2f}".format(value)

    @property
    def last_known_value(self) -> Decimal:
        if len(self.past_values) == 0:
            return Decimal(0)
        return self.past_values[-1]

    @property
    def net_worth_gain(self):
        return (self.calculate_net_worth() / self.initial_dollar_balance) - 1

    def sell(self, amount, price):
        self.balance_btc -= amount
        self.balance_dollar += amount * price

    def sell_all(self, price):
        self.sell(self.balance_btc, price)

    def buy(self, amount, price):
        self.balance_dollar -= amount * price
        self.balance_btc += amount

    def buy_all(self, price):
        amount = self.balance_dollar / price
        self.buy(amount, price)

    def calculate_net_worth(self) -> Decimal:
        if self.balance_btc.is_zero():
            balance_btc_in_dollar = 0
        else:
            balance_btc_in_dollar = self.last_known_value * self.balance_btc

        self.net_worth = self.balance_dollar + balance_btc_in_dollar

        return self.net_worth

    def print_net_worth(self):
        return f'{self} net worth U$: ' \
               f'{self.format_money(self.calculate_net_worth())}'

    def make_move(self, current_value, open_value=None, high_value=None,
                  low_value=None):
        x = []

        for s in self.strategies:
            x.append(s.get_signal(past_values=self.past_values,
                                  current_value=Decimal(current_value)))

        signal = self.model(numpy.array([x], dtype=float)).numpy()[0][0]

        if signal > 0:
            self.buy_all(current_value)
        elif signal < 0:
            self.sell_all(current_value)
        self.past_values.append(current_value)

    def __str__(self):
        return f'{self.name}'

    def copy(self):
        return MLAgent(self.name, self.model, self.strategies,
                       self.balance_dollar)
