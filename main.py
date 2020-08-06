import copy

from agent.envelopedmovingaverageagent import EnvelopedMovingAverageAgent
from agent.holdagent import HoldAgent
from agent.simplemovingaverageagent import SimpleMovingAverageAgent
from simulation import Simulation

agents = [
    HoldAgent('Hold'),
    SimpleMovingAverageAgent('Simple 14', 14),
    SimpleMovingAverageAgent('Simple 20', 20),
    EnvelopedMovingAverageAgent('Envelope 14', 14, 0.03),
    EnvelopedMovingAverageAgent('Envelope 14 tolerant', 14, 0.05),
    EnvelopedMovingAverageAgent('Envelope 20', 20, 0.03),
    EnvelopedMovingAverageAgent('Envelope 20 tolerant', 20, 0.05),
    EnvelopedMovingAverageAgent('Envelope 45', 45, 0.03),
]

simulations = [
    Simulation('BTC-USD_5Y', copy.deepcopy(agents)),
    Simulation('BTC-USD_3Y', copy.deepcopy(agents)),
    Simulation('BTC-USD_1Y', copy.deepcopy(agents)),
]

for simulation in simulations:
    simulation.play()
