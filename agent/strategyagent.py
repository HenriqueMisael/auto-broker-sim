from decimal import Decimal
from math import isclose
from typing import List

from agent.strategy.strategy import Strategy, SELL, BUY


class StrategyAgent(object):
    balance_btc: Decimal
    balance_dollar: Decimal
    past_values: List[Decimal]
    strategy: Strategy

    net_worth: Decimal
    _last_known_value: Decimal

    def __init__(self, name='Agent', strategy: Strategy = Strategy()):
        self.name = name
        self.balance_btc = Decimal(0)
        self.balance_dollar = Decimal(10000)
        self.past_values = []
        self.strategy = strategy

    @staticmethod
    def format_money(value):
        return "{:,.2f}".format(value)

    @property
    def last_known_value(self) -> Decimal:
        if len(self.past_values) == 0:
            return Decimal(0)
        return self.past_values[-1]

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

    def make_move(self, current_value):
        signal = self.strategy.get_signal(self.balance_dollar, self.past_values,
                                          current_value)
        if isclose(signal, BUY):
            self.buy_all(current_value)
        elif isclose(signal, SELL):
            self.sell_all(current_value)

        self.past_values.append(current_value)

    def __str__(self):
        return f'{self.name} ({self.strategy})'
