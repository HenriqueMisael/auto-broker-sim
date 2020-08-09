from decimal import Decimal
from typing import List

import numpy

from agent.agent import Agent

BUY = 1

SELL = -1


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


class MovingAverageAgent(Agent):
    averages: List[Average]

    def __init__(self, name, averages: List[Average]):
        super().__init__(name)
        self.averages = averages

    @property
    def upper_limit(self):
        return self.last_known_value

    @property
    def lower_limit(self):
        return self.last_known_value

    @property
    def signal(self) -> float:
        return sum(
            a.get_signal(self.past_days_close_value, self.last_known_value)
            for a in self.averages
        ) / len(self.averages)

    @property
    def should_sell_all(self) -> bool:
        return self.is_buying & numpy.isclose(self.signal, SELL)

    @property
    def should_buy_all(self) -> bool:
        return (not self.is_buying) & numpy.isclose(self.signal, BUY)

    def on_day_open(self, open_value):
        super().on_day_open(open_value)
        self.calculate_net_worth()

        if any(not a.is_ready(self.past_days_close_value)
               for a in self.averages):
            return

        if self.should_buy_all:
            self.buy_all(open_value)
        elif self.should_sell_all:
            self.sell_all(open_value)

    def __str__(self):
        return f'{self.name} {"/".join(map(lambda a: format(a.days), self.averages))} days'
