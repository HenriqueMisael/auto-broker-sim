import locale
from decimal import Decimal
from typing import List

import pandas as pd

from agent.agent import Agent

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


class Simulation(object):

    def __init__(self, file_to_import, agents: List[Agent]):
        self.file_to_import = file_to_import
        self.agents = agents
        self.agents_net_worth = []
        self.stock_day = pd.read_csv(f'source/{self.file_to_import}.csv',
                                     names=['Date', 'Open', 'High', 'Low',
                                            'Close',
                                            'Adj Close', 'Volume'],
                                     index_col='Date',
                                     header=0,
                                     float_precision=5,
                                     decimal=','
                                     )

    def play(self):
        print(f"Starting simulation {self.file_to_import}")
        for date, values in self.stock_day.iterrows():
            self.play_day(date, Decimal(values['Open']),
                          Decimal(values['Close']))

        self.export_simulation_output()
        self.export_simulation_result()

    def export_simulation_output(self):
        output = pd.DataFrame(self.agents_net_worth,
                              columns=['Date', 'Close value'] + list(
                                  map(lambda agent: agent.__str__(),
                                      self.agents)))
        output.to_csv(f'output/{self.file_to_import}.tsv', index=False,
                      sep='\t',
                      line_terminator='\n')

    def export_simulation_result(self):
        output = pd.DataFrame([self.agents_net_worth[0], self.agents_net_worth[
            len(self.agents_net_worth) - 1]],
                              columns=['Date', 'Close value'] + list(
                                  map(lambda agent: agent.name, self.agents)))
        output.to_csv(f'output/{self.file_to_import}_result.tsv', index=False,
                      sep='\t',
                      line_terminator='\n')

    def play_day(self, date, open_value, close_value):
        day_output = [date, locale.format_string('%f', close_value)]
        for agent in self.agents:
            agent.on_day_open(open_value)
            agent.on_day_close(close_value)
            day_output.append(
                locale.format_string('%f', agent.calculate_net_worth()))
        self.agents_net_worth.append(day_output)
