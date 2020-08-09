import copy

from agent.holdagent import HoldAgent
from agent.movingaverageagent import MovingAverageAgent, Average, \
    EnvelopedAverage
from simulation import Simulation

agents = [
    HoldAgent('Hold'),
    MovingAverageAgent('Simple', [Average(14)]),
    MovingAverageAgent('Simple', [Average(20)]),
    MovingAverageAgent('Enveloped 3%', [EnvelopedAverage(14, 0.03)]),
    MovingAverageAgent('Enveloped 5%', [EnvelopedAverage(14, 0.05)]),
    MovingAverageAgent('Enveloped 3%', [EnvelopedAverage(20, 0.03)]),
    MovingAverageAgent('Enveloped 5%', [EnvelopedAverage(20, 0.05)]),
    MovingAverageAgent('Enveloped 3%', [EnvelopedAverage(45, 0.03)]),
]

simulations = [
    Simulation('BTC-USD_5Y', copy.deepcopy(agents)),
    Simulation('BTC-USD_3Y', copy.deepcopy(agents)),
    Simulation('BTC-USD_1Y', copy.deepcopy(agents)),
]

for simulation in simulations:
    simulation.play()
