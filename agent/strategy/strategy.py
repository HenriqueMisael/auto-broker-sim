from decimal import Decimal
from typing import List

BUY = 1
NONE = 0
SELL = -1


class Strategy(object):
    def get_signal(self, balance_money: Decimal,
                   past_values: List[Decimal],
                   current_value: Decimal) -> float:
        return NONE

    def __str__(self):
        return 'Strategy'
