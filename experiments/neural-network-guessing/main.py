import tensorflow as tf
from numpy import genfromtxt

from agent.machinelearning.ml_agent import MLAgent
from agent.strategy.movingaverage import StrategyMovingAverage, \
    ExponentialAverage, Average, EnvelopedAverage
from agent.strategyagent import StrategyAgent
from experiments.agents_outcome_comparison.simulation import Simulation

tf.random.set_seed(11234)


def run_sim(model):
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
    simulation_builder = Simulation.Builder('../../source/BTC-USD_5Y.csv',
                                            '../../output',
                                            [StrategyAgent('Exponential',
                                                           StrategyMovingAverage(
                                                               [
                                                                   ExponentialAverage(
                                                                       7)])),
                                             MLAgent('Machine Learning', model,
                                                     strategies=strategies)])
    simulation_builder.build('2018-07-01', '2020-06-30').play()


dataset_path = "C:\\Users\\henri\\dev\\broker-prototype\\source\\BTC-USD_20days_5Y.csv"
training_proportion = 0.6


def separate_input_output(raw):
    return raw[:, :12], raw[:, -1]


dataset = genfromtxt(dataset_path, delimiter=',')
part = round(len(dataset) * training_proportion)

training, test = dataset[0:part], dataset[part:]
trainingX, trainingY = separate_input_output(training)

testX, testY = separate_input_output(test)

model = tf.keras.Sequential(
    [tf.keras.layers.Flatten(input_shape=trainingX[0].shape),
     tf.keras.layers.Dense(48, activation=tf.keras.activations.tanh),
     tf.keras.layers.Dense(24, activation=tf.keras.activations.tanh),
     tf.keras.layers.Dense(12, activation=tf.keras.activations.tanh),
     tf.keras.layers.Dense(1, activation=tf.keras.activations.tanh),
     ])

model.compile(loss=tf.keras.losses.cosine_similarity, metrics='accuracy')
model.fit(trainingX, trainingY, epochs=100, batch_size=32)
model.evaluate(testX, testY)
run_sim(model)
# tf.keras.models.save_model(model, 'model')
