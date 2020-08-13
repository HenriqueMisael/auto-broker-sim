from decimal import Decimal
from typing import List

from agent.strategy.strategy import BUY, NONE, Strategy


class StrategyHold(Strategy):

    def get_signal(self, balance_money: Decimal,
                   past_values: List[Decimal],
                   current_value: Decimal) -> float:
        if balance_money > 0:
            return BUY
        return NONE

    def __str__(self):
        return 'Hold'
