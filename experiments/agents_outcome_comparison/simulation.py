import locale
import string
from decimal import Decimal
from typing import List

import pandas as pd

from agent.strategyagent import StrategyAgent

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


class Simulation(object):
    class Builder(object):

        def __init__(self, file_to_import, dir_to_export,
                     agents: List, dbd=False, agc=False, fld=False):
            self.dir_to_export = dir_to_export
            self.stock_history = pd.read_csv(
                f'{file_to_import}',
                names=['Date', 'Open', 'High', 'Low',
                       'Close',
                       'Adj Close', 'Volume'],
                header=0,
                float_precision=5,
                decimal=','
            )
            self.agents = agents
            self.dbd = dbd
            self.agc = agc
            self.fld = fld

        def get_index_by_date(self, date):
            for i, values in self.stock_history.iterrows():
                if values['Date'] == date:
                    return i

        def build(self, start_date: string, end_date: string):
            start_index = self.get_index_by_date(start_date)
            end_index = self.get_index_by_date(end_date)

            simulation_stock_history = self.stock_history[start_index:end_index]

            return Simulation(f'{start_date} to {end_date}',
                              simulation_stock_history,
                              list(map(lambda a: a.copy(), self.agents)),
                              self.dir_to_export,
                              dbd=self.dbd,
                              agc=self.agc,
                              fld=self.fld,
                              )

    def __init__(self, name, stock_history, agents: List[StrategyAgent],
                 dir_to_export, dbd=False, agc=False, fld=False):
        self.agents = agents
        self.agents_net_worth = []
        self.name = name
        self.dir_to_export = dir_to_export
        self.stock_history = stock_history
        self.dbd = dbd
        self.agc = agc
        self.fld = fld

    def play(self):
        print(f"Starting simulation {self.name}")
        for _, values in self.stock_history.iterrows():
            open = Decimal(values['Open'])
            high = Decimal(values['High'])
            low = Decimal(values['Low'])
            close = Decimal(values['Close'])
            self.play_day(values['Date'], open, high, low, close)

        if self.dbd:
            self.export_simulation_day_by_day()
        if self.fld:
            self.export_simulation_first_last_day()
        if self.agc:
            self.export_simulation_agents_comparison()
        # self.export_simulation_monthly_gain()
        # self.calculate_statistics()

    def export_simulation_day_by_day(self):
        output = pd.DataFrame(self.agents_net_worth,
                              columns=['Date', 'Close value'] + list(
                                  map(lambda agent: agent,
                                      self.agents)))
        output.to_csv(f'{self.dir_to_export}/{self.name}_dbd.tsv', index=False,
                      sep='\t',
                      line_terminator='\n')

    def export_simulation_first_last_day(self):
        output = pd.DataFrame([self.agents_net_worth[0], self.agents_net_worth[
            len(self.agents_net_worth) - 1]],
                              columns=['Date', 'Close value'] + list(
                                  map(lambda agent: agent, self.agents)))
        output.to_csv(f'{self.dir_to_export}/{self.name}_fld.tsv', index=False,
                      sep='\t',
                      line_terminator='\n')

    def export_simulation_agents_comparison(self):
        agents_net_worth_gain = []

        first_price = Decimal(self.stock_history.iloc[0]['Close'])
        last_price = Decimal(self.stock_history.iloc[-1]['Close'])
        price_change = abs((last_price / first_price) - 1)

        self.agents.sort(key=lambda x: x.net_worth_gain, reverse=True)

        for i, agent in enumerate(self.agents):
            gain = agent.net_worth_gain
            agents_net_worth_gain.append(
                [agent.__str__(),
                 "{:.3%}".format(gain).replace('.', ','),
                 "{:.3%}".format(gain / price_change).replace('.', ',')])
        output = pd.DataFrame(
            agents_net_worth_gain,
            columns=['Agent', 'Percentage gain', 'Optimized percentage gain'])
        output.to_csv(f'{self.dir_to_export}/{self.name}_agc.tsv', index=True,
                      sep='\t',
                      line_terminator='\n')

    def play_day(self, date, open_value, high_value, low_value, close_value):
        day_output = [date, locale.format_string('%f', close_value)]
        for agent in self.agents:
            agent.make_move(close_value, open_value=open_value,
                            high_value=high_value, low_value=low_value)
            day_output.append(
                locale.format_string('%f', agent.calculate_net_worth()))
        self.agents_net_worth.append(day_output)

    @property
    def variancia(self):
        close_values = list(map(lambda x: Decimal(x[1]['Close']),
                                self.stock_history.iterrows()))
        N = len(close_values)
        average = sum(close_values) / N

        downside_risk_sum = 0
        for value in close_values:
            downside_risk_sum += (value - average) ** 2

        return downside_risk_sum / (N - 1)

    @property
    def downside_risk(self):
        close_values = list(map(lambda x: Decimal(x[1]['Close']),
                                self.stock_history.iterrows()))
        N = len(close_values)
        average = sum(close_values) / N

        downside_risk_sum = 0
        for value in close_values:
            downside_risk_sum += min(0, value - average) ** 2

        return downside_risk_sum / (N - 1)

    def calculate_statistics(self):
        print("Variância", self.variancia)
        print("Downside risk", self.downside_risk)
