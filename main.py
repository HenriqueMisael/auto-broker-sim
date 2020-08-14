import copy

from agent.strategy.movingaverage import Average, EnvelopedAverage, \
    StrategyMovingAverage
from agent.strategyagent import StrategyAgent
from simulation import Simulation

agents = [
    StrategyAgent('Simple', StrategyMovingAverage([Average(20)])),
    StrategyAgent('Enveloped',
                  StrategyMovingAverage([EnvelopedAverage(14, 0.03)])),
    StrategyAgent('Enveloped',
                  StrategyMovingAverage([EnvelopedAverage(14, 0.05)])),
    StrategyAgent('Enveloped',
                  StrategyMovingAverage([EnvelopedAverage(20, 0.05)])),
    StrategyAgent('Double', StrategyMovingAverage([Average(5), Average(20)])),
    StrategyAgent('Double', StrategyMovingAverage([Average(7), Average(14)])),
    StrategyAgent('Double',
                  StrategyMovingAverage([Average(4), Average(9), Average(18)])),
]

simulations = [
    Simulation('BTC-USD_5Y', copy.deepcopy(agents)),
    Simulation('BTC-USD_3Y', copy.deepcopy(agents)),
    Simulation('BTC-USD_1Y', copy.deepcopy(agents)),
]

for simulation in simulations:
    simulation.play()
