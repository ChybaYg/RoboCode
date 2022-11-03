import matplotlib.pyplot as plt
import numpy as np

from tensorflow.keras.models import load_model

from util import read_data

def plot(name):
    m = load_model(f'model/{name}.h5')

    data = read_data(f'training_data/{name}.csv')

    hits = data[np.where(data[:, -1] == 1)[0]]
    misses = data[np.where(data[:, -1] == 0)[0]]

    inputs = misses

    y = np.squeeze(m(inputs[:, :-1]).numpy())

    predicted_hits = inputs[np.where(y > 0.5)]
    predicted_misses = inputs[np.where(y <= 0.5)]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')

    ax.scatter(predicted_hits[:, 0], predicted_hits[:, 1], predicted_hits[:, 2], marker = 'o')
    # ax.scatter(predicted_misses[:, 0], predicted_misses[:, 1], predicted_misses[:, 2], marker = 'o')
    ax.scatter(hits[:, 0], hits[:, 1], hits[:, 2], marker = '^')

    ax.set_xlabel('gun to rotate')
    ax.set_ylabel('distance')
    ax.set_zlabel('angle')

plot('sitting_duck')
# plot('walls')

plt.show()