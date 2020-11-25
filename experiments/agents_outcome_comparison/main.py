from datetime import datetime

import tensorflow as tf

from agent.machinelearning.ml_agent import MLAgent
from agent.strategy.movingaverage import Average, EnvelopedAverage, \
    StrategyMovingAverage, ExponentialAverage
from agent.strategyagent import StrategyAgent
from experiments.agents_outcome_comparison.simulation import Simulation

strategies = [
    StrategyMovingAverage(
        [Average(14)]),
    StrategyMovingAverage(
        [Average(20)]),
    StrategyMovingAverage([
        EnvelopedAverage(
            14,
            0.03)]),
    StrategyMovingAverage([
        EnvelopedAverage(
            14,
            0.05)]),
    StrategyMovingAverage([
        EnvelopedAverage(
            20,
            0.03)]),
    StrategyMovingAverage([
        EnvelopedAverage(
            20,
            0.05)]),
    StrategyMovingAverage(
        [Average(7),
         Average(14)]),
    StrategyMovingAverage(
        [Average(5),
         Average(20)]),
    StrategyMovingAverage(
        [Average(4),
         Average(9),
         Average(18)]),
    StrategyMovingAverage([
        ExponentialAverage(
            7)]),
    StrategyMovingAverage([
        ExponentialAverage(
            14)]),
    StrategyMovingAverage([
        ExponentialAverage(
            20)]),
]

model = tf.keras.models.load_model('../neural-network-guessing/model')

agents = [
    StrategyAgent('Simple', StrategyMovingAverage([Average(14)])),
    StrategyAgent('Simple', StrategyMovingAverage([Average(20)])),
    StrategyAgent('Enveloped',
                  StrategyMovingAverage([EnvelopedAverage(14, 0.03)])),
    StrategyAgent('Enveloped',
                  StrategyMovingAverage([EnvelopedAverage(14, 0.05)])),
    StrategyAgent('Enveloped',
                  StrategyMovingAverage([EnvelopedAverage(20, 0.03)])),
    StrategyAgent('Enveloped',
                  StrategyMovingAverage([EnvelopedAverage(20, 0.05)])),
    StrategyAgent('Double',
                  StrategyMovingAverage([Average(7), Average(14)])),
    StrategyAgent('Double',
                  StrategyMovingAverage([Average(5), Average(20)])),
    StrategyAgent('Triple',
                  StrategyMovingAverage([Average(4), Average(9), Average(18)])),
    StrategyAgent('Exponential',
                  StrategyMovingAverage([ExponentialAverage(7)])),
    StrategyAgent('Exponential',
                  StrategyMovingAverage([ExponentialAverage(14)])),
    StrategyAgent('Exponential',
                  StrategyMovingAverage([ExponentialAverage(20)])),
]

simulation_builder = Simulation.Builder('../../source/BTC-USD_5Y.csv',
                                        '../../output', agents)


def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')


simulations = [
    simulation_builder.build('2015-07-01', '2016-06-30'),
    simulation_builder.build('2016-07-01', '2017-06-30'),
    simulation_builder.build('2017-07-01', '2018-06-30'),
    simulation_builder.build('2018-07-01', '2019-06-30'),
    simulation_builder.build('2019-07-01', '2020-06-30'),
]

for simulation in simulations:
    simulation.play()
