from decimal import Decimal

from agent.simplemovingaverageagent import SimpleMovingAverageAgent


class EnvelopedMovingAverageAgent(SimpleMovingAverageAgent):
    envelope: Decimal

    def __init__(self, name, days, envelope):
        super().__init__(name, days)
        self.envelope = Decimal(envelope)

    @property
    def upper_limit(self):
        return self.last_known_value * (1 + self.envelope)

    @property
    def lower_limit(self):
        return self.last_known_value * (1 - self.envelope)

    def should_sell_all(self, moving_average) -> bool:
        return self.is_buying & (moving_average > self.upper_limit)

    def should_buy_all(self, moving_average) -> bool:
        return (not self.is_buying) & (moving_average < self.lower_limit)
