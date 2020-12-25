from tensorflow import keras

from agent.machinelearning.price_ml_agent import PriceMLAgent
from experiments.agents_outcome_comparison.simulation import Simulation

agent = PriceMLAgent('Price based', keras.models.load_model("output/model"))
simulation = Simulation.Builder('../../source/BTC-USD_5Y.csv',
                                'output',
                                [agent],
                                fld=True).build('2019-07-01', '2020-06-30')
simulation.play()

results = list(
    map(lambda a: [
        a.name,
        round(float(a.net_worth), 2),
    ],
        simulation.agents))
print(results)
