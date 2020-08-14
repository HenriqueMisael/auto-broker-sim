from decimal import Decimal
from typing import List

from agent.strategy.strategy import BUY, SELL, Strategy


class Average(object):
    days: int

    def __init__(self, days):
        self.days = days

    def calculate(self, values: List[Decimal]):
        return sum(values[-self.days:]) / self.days

    def is_ready(self, values: List[Decimal]):
        return len(values) >= self.days

    def get_signal(self, values: List[Decimal], current_price: Decimal):
        moving_average = self.calculate(values)

        if moving_average < current_price:
            return BUY
        elif moving_average > current_price:
            return SELL
        return 0

    def __str__(self):
        return f'{self.days}'


class EnvelopedAverage(Average):
    envelope: Decimal

    def __init__(self, days, envelope):
        super().__init__(days)
        self.envelope = Decimal(envelope)

    def get_signal(self, values: List[Decimal], current_price: Decimal):
        moving_average = self.calculate(values)

        if moving_average < (current_price * (1 - self.envelope)):
            return BUY
        elif moving_average > (current_price * (1 + self.envelope)):
            return SELL
        return 0

    def __str__(self):
        return f'{"{:.1%}".format(self.envelope)} {self.days}'


class StrategyMovingAverage(Strategy):

    def __init__(self, averages: List[Average]):
        self.averages = averages

    def get_signal(self, balance_money: Decimal,
                   past_values: List[Decimal],
                   current_value: Decimal) -> float:
        return sum(
            a.get_signal(past_values, current_value)
            for a in self.averages
        ) / len(self.averages)

    def __str__(self):
        return f'{"/".join(a.__str__() for a in self.averages)}'
