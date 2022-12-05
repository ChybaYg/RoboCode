import tensorflow.keras as keras
import pandas as pd

from robocodeAIServer import number_of_fields, scale_values


dataset_name = "data_for_game.csv"
model_name = "data_for_game.keras"
num_empochs = 100
batch_size = 64
validation_split = 0.01
equalize_hits = True
save_filtered_dataset = True


def main():
    # Load dataset from csv file
    df = pd.read_csv(dataset_name, delimiter=";", dtype="float", decimal=".")

    if equalize_hits:
        print("=========================================================")
        print("Dataset before filtration")
        print("---------------------------------------------------------")
        print(df)

        # Sort dataset according to hits
        df = df.sort_values(by=['hit'])

        # Get number of hits
        hits_enemy = len(df[df['hit'] == 1])
        # Get number of misses
        miss_hit = len(df[df['hit'] == 0])
        print("---------------------------------------------------------")
        if hits_enemy > miss_hit:
            diff = hits_enemy - miss_hit
            class_weight = {0:hits_enemy/miss_hit,1:1}
            print(f"There are {diff} more hitting enemy than missing hits")
        elif miss_hit > hits_enemy:
            diff = miss_hit - hits_enemy
            class_weight = {0:1,1:miss_hit/hits_enemy}
            print(f"There are {diff} more missing hits than hitting enemy")


        # Random order
        df = df.sample(frac=1).reset_index(drop=True)

        if save_filtered_dataset:
            df.to_csv("filtered.csv", sep=";", index=False, decimal=",")

    # Scale values between 0 and 1
    if scale_values:
        df["distX"] /= 800
        df["distY"] /= 600
        df["myGunHeading"] /= 360
        df["velocityX"] /= 8
        df["velocityY"] /= 8


    print("=========================================================")
    print("Dataset")
    print("---------------------------------------------------------")
    print(df)

    # training data
    X = df.iloc[:, : (number_of_fields-1)]
    print("=========================================================")
    print("Training data")
    print("---------------------------------------------------------")
    print(X)

    # predicated data
    y = df.iloc[:,-1]
    print("=========================================================")
    print("Predicated data")
    print("---------------------------------------------------------")
    print(y)
    print("=========================================================")

    # initialize mode
    m = keras.Sequential([
        keras.layers.Input(shape=(number_of_fields-1)),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid'),
    ])

    print(m.summary())

    # optimizer for correcting weights in machine learning, loss function for calculating mistakes
    m.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # train and evaluate
    
    m.fit(X, y, epochs=num_empochs, batch_size=batch_size, validation_split=validation_split, class_weight=class_weight)

    # save model
    m.save(model_name)

    _, accuracy = m.evaluate(X, y)
    print("=========================================================")
    print('Accuracy: %.2f' % (accuracy * 100))
    print("=========================================================")


if __name__ == '__main__':
    main()