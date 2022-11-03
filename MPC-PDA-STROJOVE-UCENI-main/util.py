import numpy as np
from csv import reader, writer
from sys import argv

number_of_inputs = 5

def read_data(file_name):
    with open(file_name, 'r') as file:
        data = np.array(list(reader(file, delimiter = ';'))).astype(np.float32)
        np.random.shuffle(data)
        return data

# filtering similar observated data (the same number of hits and misses is needed bcs of learning - learn the same number when you hit or lose to avoid overtrain)
def filter_data(file_name):
    data = read_data(f'{file_name}.csv')

    hits = _filter(data[np.where(data[:, -1] == 1)[0]], 0.001)
    misses = _filter(data[np.where(data[:, -1] == 0)[0]], 0.2)

    # make sure theres even number of hits as misses
    misses = misses[:hits.shape[0]]
    hits = hits[:misses.shape[0]]

    with open(f'{file_name}_filtered.csv', 'w' if len(argv) == 1 else 'a') as file:
        writer(file, delimiter = ';').writerows(np.append(hits, misses, axis = 0))

def _filter(data, threshold):
    i = 0
    while i < data.shape[0] - 1:
        print(i, data.shape[0])
        indexes = _similar_indexes(data[i], data[i + 1:], threshold)
        
        data = np.delete(data, indexes, axis = 0)

        i += 1
    
    return data

def _similar_indexes(x, y, threshold):
    return np.where(np.abs(np.sum(np.abs(y[:, :number_of_inputs] - x[:number_of_inputs]), axis = 1)) < threshold)[0]

if __name__ == '__main__':
    filter_data('observations')
