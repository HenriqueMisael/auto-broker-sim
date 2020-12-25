from dataclasses import dataclass
from typing import List

import tensorflow as tf

from agent.machinelearning.ml_agent import MLAgent
from datageneration import strategy_based_data, expected_output, get_strategies
from experiments.agents_outcome_comparison.simulation import Simulation

tf.random.set_seed(20201217)

keras = tf.keras

x = strategy_based_data()
y = expected_output()

part = int(len(x) * 3/5)
train_x, test_x = x[:part], x[part:]
train_y, test_y = y[:part], y[part:]


@dataclass
class TestLayerOpt:
    dropout: float
    units: int
    activation: str

    def __init__(self, units, dropout=None, activation='tanh'):
        self.units = units
        self.dropout = dropout
        self.activation = activation


@dataclass
class TestArgs:
    name: str
    epoch_count: int

    def __init__(self, epoch_count=1, lr=0.001, layers=None,
                 losses=None, metrics=None, name=None):
        if metrics is None:
            metrics = ['accuracy']
        if losses is None:
            losses = ['mean_squared_error']
        self.lr = lr
        self.layers = layers
        self.name = str(epoch_count) if name is None else name
        self.epoch_count = epoch_count
        self.losses = losses
        self.metrics = metrics


def create_model_strategies(epochs,
                            layers_opt: List[TestLayerOpt],
                            learning_rate,
                            losses,
                            metrics):
    layers = []
    for i, lo in enumerate(layers_opt):
        isFirst = i == 0
        isDropout = lo.dropout is not None
        input_shape = train_x[0].shape
        if isDropout:
            if isFirst:
                layers.append(
                    keras.layers.Dropout(lo.dropout, input_shape=input_shape))
            else:
                layers.append(keras.layers.Dropout(lo.dropout))
        if isFirst and not isDropout:
            layers.append(keras.layers.Dense(lo.units, input_shape=input_shape,
                                             activation=lo.activation))
        else:
            layers.append(
                keras.layers.Dense(lo.units, activation=lo.activation))

    new_model = keras.models.Sequential(layers=layers)
    adam = keras.optimizers.Adam(learning_rate=learning_rate)
    new_model.compile(adam, losses, metrics)
    new_model.fit(train_x, train_y, epochs=epochs)
    # new_model.evaluate(test_x, test_y)

    return new_model


def create_test_agent(test_args: TestArgs):
    model = create_model_strategies(test_args.epoch_count,
                                    test_args.layers,
                                    test_args.lr,
                                    test_args.losses,
                                    test_args.metrics)
    agent = MLAgent(test_args.name, model, get_strategies())

    return agent


def run_many_tests(tests_args: List[TestArgs]):
    agents = []
    for test_args in tests_args:
        agent = create_test_agent(test_args)
        agents.append(agent)

    simulation = Simulation.Builder('../../source/BTC-USD_5Y.csv',
                                    'output',
                                    agents,
                                    fld=True).build('2018-07-01', '2019-06-30')
    simulation.play()

    results = list(
        map(lambda a: [
                          a.name,
                          round(float(a.net_worth), 2),
                      ] + a.model.evaluate(test_x, test_y),
            simulation.agents))
    print(
        results.__str__()
            .replace(', ', '\t')
            .replace(']\t[', '\n')
            .replace('[[', '')
            .replace(']]', ''))


epochs = [1, 2, 4, 8, 16, 32, 64, 128]
units = [144, 72, 36, 1]
learning_rates = [0.001, 0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
losses = ['mean_squared_error', 'poisson', 'kl_divergence']
metrics = ['accuracy']
keras.optimizers.Adam
tests = []
for e in epochs:
    # No dropout
    for lr in learning_rates:
        for loss in losses:
            layers = []
            for u in units:
                layers.append(TestLayerOpt(u))
            tests.append(
                TestArgs(e, lr, name=f'{e}|{lr}|{loss}|None', losses=loss,
                         metrics=metrics,
                         layers=layers))
    # Input dropout 20%
    for lr in learning_rates:
        for loss in losses:
            layers = []
            for i, u in enumerate(units):
                dropout = 0.2 if i == 0 else None
                layers.append(TestLayerOpt(u, dropout))
            tests.append(
                TestArgs(e, lr, name=f'{e}|{lr}|{loss}|In20_None', losses=loss,
                         metrics=metrics,
                         layers=layers))
    # Input dropout 20%, then 20%
    for lr in learning_rates:
        for loss in losses:
            layers = []
            for i, u in enumerate(units):
                dropout = None
                if i == 0 or i == 1:
                    dropout = 0.2
                layers.append(TestLayerOpt(u, dropout))
            tests.append(
                TestArgs(e, lr, name=f'{e}|{lr}|{loss}|In20_20_None', losses=loss,
                         metrics=metrics,
                         layers=layers))
    # Dropout 20% in every layer
    for lr in learning_rates:
        for loss in losses:
            layers = []
            for i, u in enumerate(units):
                dropout = 0.2
                layers.append(TestLayerOpt(u, dropout))
            tests.append(
                TestArgs(e, lr, name=f'{e}|{lr}|{loss}|All20', losses=loss,
                         metrics=metrics,
                         layers=layers))
    # Input dropout 20%, then 10%
    for lr in learning_rates:
        for loss in losses:
            layers = []
            for i, u in enumerate(units):
                dropout = None
                if i == 0:
                    dropout = 0.2
                if i == 1:
                    dropout = 0.1
                layers.append(TestLayerOpt(u, dropout))
            tests.append(
                TestArgs(e, lr, name=f'{e}|{lr}|{loss}|In20_10_None', losses=loss,
                         metrics=metrics,
                         layers=layers))
    # Input dropout 20%, then 10% and 5%
    for lr in learning_rates:
        for loss in losses:
            layers = []
            for i, u in enumerate(units):
                dropout = None
                if i == 0:
                    dropout = 0.2
                if i == 1:
                    dropout = 0.1
                if i == 2:
                    dropout = 0.05
                layers.append(TestLayerOpt(u, dropout))
            tests.append(
                TestArgs(e, lr, name=f'{e}|{lr}|{loss}|In20_10_5', losses=loss,
                         metrics=metrics,
                         layers=layers))

run_many_tests(tests)
