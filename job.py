import helpers

from step import Step

class Job:
    def __init__(self, name, context=None):
        self.name = name
        self.steps = []
        self.context = context

    def add_step(self, step: Step):
        self.steps.append(step)

    def run_steps(self):
        for step in self.steps:
            if not step.execute(self.context):
                print(f"Step {step.name} failed")
                return False

        return True

    def __str__(self):
        text = f"Job: {self.name}\n"
        for step in self.steps:
            text += f"\t{str(step)}\n"
        return text