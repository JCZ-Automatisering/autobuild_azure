import os


class Environment:
    def __init__(self, filename):
        self.filename = filename
        self.environment = {}

        if not os.path.exists(filename):
            return

        with open(self.filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                split = line.split("=", maxsplit=1)
                if len(split) == 2:
                    key = split[0].strip()
                    value = split[1].strip()
                    self.environment[key] = value
