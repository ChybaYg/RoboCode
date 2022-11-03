import tensorflow.keras as keras
import pandas as pd

from robocodeAIServer import number_of_fields, scale_values


dataset_name = "dataset.csv"
model_name = "crazy.keras"
num_empochs = 2
batch_size = 4
validation_split = 0.01
equalize_hits = True
save_filtered_dataset = True


def main():
    # Load dataset from csv file
    df = pd.read_csv(dataset_name, delimiter=";", dtype="float", decimal=",")

    if equalize_hits:
        print("dataset before filtration")
        print(df)

        # Sort dataset according to hits
        df = df.sort_values('hit')

        # Get number of hits
        hits = len(df[df['hit'] == 1])
        # Get number of misses
        not_hits = len(df[df['hit'] == 0])
        diff = not_hits - hits
        print(f"there are {diff} diff more not hits than hits")

        # Remove misses
        df = df.iloc[diff:, :]

        # Random order
        df = df.sample(frac=1).reset_index(drop=True)

        if save_filtered_dataset:
            df.to_csv("filtered.csv", sep=";", index=False, decimal=",")

    # Scale values between 0 and 1
    if scale_values:
        df["x"] /= 800
        df["y"] /= 600
        df["gunHeading"] /= 360
        df["enemyDistance"] /= 1000
        df["enemyHeading"] /= 360
        df["enemyVelocity"] /= 8  # -1 to 1

    print("Dataset")
    print(df)

    # training data
    X = df.iloc[:, : (number_of_fields-1)]
    print("training data")
    print(X)

    # predicated data
    y = df.iloc[:,-1]
    print("predicated data")
    print(y)

    # initialize mode
    m = keras.Sequential([
        keras.layers.Input(shape=(number_of_fields-1)),
        keras.layers.Dense(28, activation='relu'),
        keras.layers.Dense(number_of_fields-1, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ])

    # optimizer for correcting weights in machine learning, loss function for calculating mistakes
    m.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

    # train and evaluate
    m.fit(X, y, epochs=num_empochs, batch_size=batch_size, validation_split=validation_split)

    # save model
    m.save(model_name)


if __name__ == '__main__':
    main()