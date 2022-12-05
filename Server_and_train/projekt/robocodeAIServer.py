import socket
import csv
import os
import numpy as np
import tensorflow.keras as keras


# You can change
ai_model_name = "data_for_game.keras"
dataset_file_name = "data_for_game.csv"
learning_game = False
model_exist = True

show_decisions = True
scale_values = True  # Values scaled between 0 and 1
confidence_constant = 0.5
# Do not change
host = "localhost"
port = 1000  # initiate port not above 1024
dataset_fields = ['distX', 'distY', 'myGunHeading','velocityX','velocityY', 'hit']
number_of_fields = len(dataset_fields)
number_of_rounds = 0


def server_program(server_socket, model):
    states = []
    conn, address = server_socket.accept()  # accept new connection
    print("New robocode game from: " + str(address))
    
    #learning state
    if learning_game:
        print(f"battle number: {number_of_rounds} battle mode: learning (waiting for data dump)")
        while True:
                try:
                    data = conn.recv(1024)
                except ConnectionResetError:
                    print("Robocode disconnected")
                    break
                if not data:
                    break
                data = data.decode()
        
                if "\r\n" in data:
                    for state in data.split('\r\n'):
                        s = state.split(';')
                    if len(s) == number_of_fields:
                            states.append(s)
                else:
                    for state in data.split('\n'):
                        s = state.split(';')
                        if len(s) == number_of_fields:
                            states.append(s)

    #AI state
    if not learning_game:
        print(f"battle number: {number_of_rounds}  battle mode: AI (sending commands)")
        while True:
            try:
                data = conn.recv(1024)
            except ConnectionResetError:
                print("Robocode disconnected")
                break
            if not data:
                break

            data = data.decode()
            if "," in data:
                data = data.replace(",", ".")
            state = data.split(';')
            ar = np.array([state]).astype(float)

            # Normalize
            if scale_values:
                # 'distX', 'distY', 'myGunHeading','velocityX', 'velocityY'
                ar[0][0] /= 800
                ar[0][1] /= 600
                ar[0][2] /= 360
                ar[0][3] /= 8
                ar[0][4] /= 8
                

            command = "do not shoot\n"
            if model:
                # Predict
                are_u_sure = model.predict(ar)
                if are_u_sure[0][0] > confidence_constant:
                    command = "shoot\n"
                if show_decisions:
                    print(f"Received data: {data} ->  confidence {are_u_sure[0][0]} decision: {command}")
            else:
                command = "shoot\n"
                if show_decisions:
                    print(f"Received data: {data} ->  confidence 1 (model missing) decision: {command}")
            conn.send(command.encode())  # send data to the client

        conn.close()  # close the connection

    if states:
        # This game was learning game save states.
        with open(dataset_file_name, "a") as file:
            writer = csv.writer(file, delimiter=";", lineterminator='\n')
            writer.writerows(states)

def main():
    print("Starting Robocode Server...", host, port)
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)

    # Create dataset file if not existent.
    if not os.path.exists(dataset_file_name):
        with open(dataset_file_name, "w") as file:
            print("Dataset file does not exist. Creating one!")
            pass

    # Check if model exists
    global model_exist
    if not os.path.exists(ai_model_name):
        print(f"Model file: {ai_model_name} does not exist! You can train model with script: train_model.py")
        model_exist = False

    # Load AI model
    if model_exist:
        model = keras.models.load_model(ai_model_name)
    else:
        model = None

    # Loop over game rounds
    while True:
        if learning_game:
            # print number of states in dataset and append new states.
            with open(dataset_file_name, "r+") as file:
                num_rows = sum(1 for row in file)
                if num_rows == 0:
                    writer = csv.writer(file, delimiter=";", lineterminator='\n')
                    writer.writerow(dataset_fields)
                    num_rows = 1
                print(f"file {dataset_file_name} has: {num_rows - 1} states.")

        try:
            server_program(server_socket, model)
        except KeyboardInterrupt:
            print("Stopping server")
            exit()
        except ConnectionResetError:
            print("ConnectionResetError")
            continue


if __name__ == '__main__':
    main()
