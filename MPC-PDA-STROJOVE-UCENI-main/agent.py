from json import loads
from random import randint

import numpy as np

from action import Action
from state import Event, Info, State
from util import number_of_inputs

class Agent:
    # model loading
    def __init__(self, model = None, training = False):
        self.model = model
        self.training = training or model == None
        self.gun_offset = -30

    # game loop once client/robot is connected
    def run(self, conn):
        self.running = True
        self.should_shoot = False
        self.conn = conn

        self.last_shoot = 0
        self.angle = 0

        while self.running:
            try:
                data = self.conn.recv(1024)
            except ConnectionResetError:
                break

            if not data:
                break
                
            messages = data.split(b'\n')

            for message in messages:
                if not message:
                    continue

                message = loads(message)

                if message['message_type'] == 'INFO':
                    self.on_start(Info(message))
                elif message['message_type'] == 'STATE':
                    self.on_turn(State(message))
                elif message['message_type'] == 'EVENT':
                    self.on_event(Event(message))
                else:
                    print(f'Received unsupported data: {data}')

        self.conn.close()

    def on_start(self, info):
        print(f'Info: {info}')

    def on_turn(self, state):
        # when is turn on robot, it is turning gun and radar in 360 degrees
        actions = [Action('TURN_GUN', -360 if self.training else self.angle), Action('TURN_RADAR', -360)]

        # when is decided - fire the bullet
        if self.should_shoot or (self.training and state.timestamp - self.last_shoot > 150):
            actions.append(Action('FIRE', 1))
            self.should_shoot = False

            self.last_shoot = state.timestamp

        self.angle = 0
        self.move = 0

        self._send_actions(actions)

    def on_event(self, event):
        if event.event_type == 'SCANNED':
            if self.model == None:
                self.should_shoot = True
            else:
                observation = np.array([
                    event.observation['gun_to_turn'], 
                    event.observation['distance'],
                    event.observation['angle'],
                    event.observation['remaining_to_wall'],
                    # event.observation['enemy_dx'],
                    # event.observation['enemy_dy'],
                    event.observation['enemy_heading']
                ]).astype(np.float32).reshape((1, number_of_inputs))

                self.angle = event.observation['gun_to_turn'] * -180 + self.gun_offset

                # when is chance of hit enemy 75 percent - fire, it can be 50% but 75% is for better results
                threshold = 0.25 if self.training else 0.75

                if np.squeeze(self.model(observation)) > threshold:
                    self.should_shoot = True
        elif event.event_type == 'ROUND_END':
            self.running = False


    def _send_actions(self, actions):
        self.conn.send(f'[{", ".join([action.dump() for action in actions])}]\n'.encode('utf8'))
