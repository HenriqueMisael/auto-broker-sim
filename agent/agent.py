from decimal import Decimal


class Agent(object):
    balance_btc: Decimal
    balance_dollar: Decimal

    net_worth: Decimal
    _last_known_value: Decimal

    def __init__(self, name='Agent'):
        self.name = name
        self.balance_btc = Decimal(0)
        self.balance_dollar = Decimal(10000)
        self.past_days_close_value = []

    @staticmethod
    def format_money(value):
        return "{:,.2f}".format(value)

    @property
    def last_known_value(self) -> Decimal:
        return self._last_known_value

    @last_known_value.setter
    def last_known_value(self, value):
        self._last_known_value = value
        pass

    @property
    def is_buying(self):
        return self.balance_btc > self.balance_dollar

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

    def __str__(self):
        return self.name

    def on_day_open(self, open_value: Decimal):
        self.last_known_value = open_value

    def on_day_close(self, close_value: Decimal):
        self.last_known_value = close_value
        self.past_days_close_value.append(close_value)
