from decimal import Decimal

from agent.agent import Agent


class HoldAgent(Agent):

    def on_day_open(self, open_value: Decimal):
        if not self.is_buying:
            self.buy_all(open_value)
