from sklearn import svm, neighbors
from pickle import dump, load

import numpy as np

class SVMModel:
    def __init__(self, file_name = None):
        if file_name == None:
            self.classifier = svm.SVC()
        else:
            with open(file_name, 'rb') as file:
                self.classifier = load(file)

    def __call__(self, X):
        # converting output to numpy array, so it acts same as tensorflow output
        return np.squeeze(np.array(self.classifier.predict(X)))

    def fit(self, X, y):
        self.classifier.fit(X, y)

    def save(self, file_name):
        with open(file_name, 'wb') as file:
            dump(self.classifier, file)

class KNNModel:
    def __init__(self, file_name = None):
        if file_name == None:
            self.classifier = neighbors.KNeighborsClassifier(n_neighbors = 3)
        else:
            with open(file_name, 'rb') as file:
                self.classifier = load(file)

    def __call__(self, X):
        # converting output to numpy array, so it acts same as tensorflow output
        return np.squeeze(np.array(self.classifier.predict(X)))

    def fit(self, X, y):
        self.classifier.fit(X, y)

    def save(self, file_name):
        with open(file_name, 'wb') as file:
            dump(self.classifier, file)