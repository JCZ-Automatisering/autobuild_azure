import helpers


class Step:
    def __init__(self, name, action):
        self.name = name
        self.action = action

    def execute(self, context = None):
        helpers.execute(self.action, True)
        return True

    def __str__(self):
        return f"step: {self.name}, action: {self.action}"

