from decimal import Decimal
from typing import List

BUY = 1
NONE = 0
SELL = -1


class Strategy(object):
    def get_signal(self, balance_money: Decimal = Decimal(0),
                   past_values: List[Decimal] = None,
                   current_value: Decimal = Decimal(0)) -> float:
        return NONE

    def __str__(self):
        return 'Strategy'
