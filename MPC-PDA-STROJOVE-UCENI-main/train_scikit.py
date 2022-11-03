from models import SVMModel, KNNModel
from util import read_data, number_of_inputs

data = read_data('training_data/walls.csv')

# divide loaded data to inputs and outputs
X = data[:, :number_of_inputs]
y = data[:, -1]

model = SVMModel()

model.fit(X, y)

model.save('model/walls_svm.pkl')


model = KNNModel()

model.fit(X, y)

model.save('model/walls_knn.pkl')