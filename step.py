import helpers
from docker import Docker


class Step:
    def __init__(self, name, action):
        self.name = name
        self.action = action

    def __execute_in_context(self, context):
        return context.run_once(self.action)

    def execute(self, context=None):
        if context:
            return self.__execute_in_context(context)

        helpers.execute(self.action, True)
        return True

    def __str__(self):
        return f"step: {self.name}, action: {self.action}"

