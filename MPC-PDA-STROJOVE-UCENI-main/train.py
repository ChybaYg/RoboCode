import numpy as np
import tensorflow.keras as keras

from util import read_data, number_of_inputs

#define model of machine learning via tensorflow library
data = read_data('observations_filtered.csv')

# divide loaded data to inputs and outputs
X = data[:, :number_of_inputs]
#predicated data
y = data[:, -1]

# initialize mode
m = keras.Sequential([
    keras.layers.Input(shape = (number_of_inputs,)),
    keras.layers.Dense(28, activation = 'relu'),
    keras.layers.Dense(7, activation = 'relu'),
    keras.layers.Dense(1, activation = 'sigmoid'),
])

# optimizer for correcting weights in machine learning, loss function for calculating mistakes
m.compile(optimizer = 'adam', loss = 'mse', metrics = ['accuracy'])

# load previous
# m = keras.models.load_model('model/walls.h5')

# train and evaluate
m.fit(X, y, epochs = 30, batch_size = 4, validation_split = 0.1)

# save model
m.save('model/walls.h5')
