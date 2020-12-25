import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler

from agent.machinelearning.price_ml_agent import PriceMLAgent
from experiments.agents_outcome_comparison.simulation import Simulation

tf.random.set_seed(20201217)

scaler = MinMaxScaler(feature_range=(0, 1))


def create_model():
    # Initialising the RNN
    new_model = Sequential()
    # Adding the first LSTM layer and some Dropout regularisation
    new_model.add(
        LSTM(units=50, return_sequences=True,
             input_shape=(20, 1)))
    new_model.add(Dropout(0.2))
    # Adding a second LSTM layer and some Dropout regularisation
    new_model.add(LSTM(units=50, return_sequences=True))
    new_model.add(Dropout(0.2))
    # Adding a third LSTM layer and some Dropout regularisation
    new_model.add(LSTM(units=50, return_sequences=True))
    new_model.add(Dropout(0.2))
    # Adding a fourth LSTM layer and some Dropout regularisation
    new_model.add(LSTM(units=50))
    new_model.add(Dropout(0.2))
    # Adding the output layer
    new_model.add(Dense(units=1))
    # Compiling the RNN
    new_model.compile(optimizer='adam', loss='mean_squared_error')

    return new_model


def load_data():
    return pd.read_csv('../../source/BTC-USD_5Y_prev20_aft1.csv')


def last_training_index():
    return 1482


def load_train_data():
    df = load_data()
    cut = last_training_index()
    return df.iloc[:cut]


def load_test_data():
    df = load_data()
    cut = last_training_index() - 19
    return df.iloc[cut:]


def split_x_y(dataset: pd.DataFrame):
    set = dataset.iloc[:, 1:5].to_numpy()
    set_scaled = scaler.fit_transform(set)
    x_train = []
    y_train = []
    for i in range(20, len(set)):
        x_train.append(set_scaled[i - 20:i, 0])
        y_train.append(set_scaled[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    return x_train, y_train


def create_train_new_model():
    dataset_train = load_train_data()
    x_train, y_train = split_x_y(dataset_train)
    model = create_model()
    model.fit(x_train, y_train, epochs=100)
    dataset_test = load_test_data()
    real_stock_price = dataset_test.iloc[:, 4:5].values
    x_test, y_test = split_x_y(dataset_test)
    predicted_stock_price = model.predict(x_test)
    predicted_stock_price = np.c_[
        predicted_stock_price, np.zeros(len(predicted_stock_price)), np.zeros(
            len(predicted_stock_price)), np.zeros(len(predicted_stock_price))]
    predicted_stock_price = scaler.inverse_transform(predicted_stock_price)[:,
                            0]
    # Visualising the results
    plt.plot(real_stock_price, color='red', label='Real BTC Close Values')
    plt.plot(predicted_stock_price, color='blue',
             label='Predicted BTC Close Values')
    plt.title('BTC Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('BTC Close Value')
    plt.legend()
    plt.show()

    model.save("output/model")
    return model


def load_model():
    return tf.keras.models.load_model('output/model')


def run_simulation(model):
    agent = PriceMLAgent('Price based', model, scaler=scaler)
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


# run_simulation(load_model())
# run_simulation(create_train_new_model())
# model = create_train_new_model()
model = load_model()
