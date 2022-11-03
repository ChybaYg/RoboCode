from json import dumps

class Action:
    def __init__(self, action_type, value):
        self.action_type = action_type
        self.value = value

    def dump(self):
        return dumps(self.__dict__)