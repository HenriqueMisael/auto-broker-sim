from agent.agent import Agent


class SimpleMovingAverageAgent(Agent):
    days: int

    def __init__(self, name, days):
        super().__init__(name)
        self.days = days

    @property
    def upper_limit(self):
        return self.last_known_value

    @property
    def lower_limit(self):
        return self.last_known_value

    def should_sell_all(self, moving_average) -> bool:
        return self.is_buying & (moving_average > self.lower_limit)

    def should_buy_all(self, moving_average) -> bool:
        return (not self.is_buying) & (moving_average < self.upper_limit)

    def on_day_open(self, open_value):
        super().on_day_open(open_value)
        self.calculate_net_worth()

        if len(self.past_days_close_value) < self.days:
            return

        moving_average = sum(self.past_days_close_value) / self.days

        if self.should_buy_all(moving_average):
            self.buy_all(open_value)
        elif self.should_sell_all(moving_average):
            self.sell_all(open_value)

    def on_day_close(self, close_value):
        super().on_day_close(close_value)
        if len(self.past_days_close_value) > self.days:
            self.past_days_close_value.pop(0)
