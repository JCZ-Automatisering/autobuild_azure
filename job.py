import helpers

from step import Step

class Job:
    def __init__(self, name):
        self.name = name
        self.steps = []

    def add_step(self, step: Step):
        self.steps.append(step)

    def run_steps(self, context = None):
        for step in self.steps:
            if not step.execute(context):
                print(f"Step {step.name} failed")
                return False

        return True

    def __str__(self):
        text = f"Job: {self.name}\n"
        for step in self.steps:
            text += f"\t{str(step)}\n"
        return text