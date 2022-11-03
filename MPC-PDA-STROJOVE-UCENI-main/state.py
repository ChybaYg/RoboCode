class Info:
    def __init__(self, data):
        self.size = (data['width'], data['height'])

    def __str__(self):
        return f'{self.size}'

class State:
    def __init__(self, data):
        self.timestamp = data['timestamp']

    def __str__(self):
        return f'{self.timestamp}'

class Event:
    def __init__(self, data):
        self.event_type = data['event_type']
        if 'observation' in data:
            self.observation = data['observation']