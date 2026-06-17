import os

from step import Step

class Job:
    def __init__(self, name, context=None):
        self.name = name
        self.steps = []
        self.context = context

    def add_step(self, step: Step):
        self.steps.append(step)

    def run_steps(self):
        skip = os.getenv("SKIP", "").split(",")
        no_docker = os.getenv("NO_DOCKER", "").split(",")
        for step in self.steps:
            if step.name in skip:
                print(f" skipping step {step} due to SKIP environment variable")
                continue
            if step.name in no_docker:
                context = None
            else:
                context = self.context
            if not step.execute(context):
                print(f"Step {step.name} failed")
                return False

        return True

    def __str__(self):
        text = f"Job: {self.name}\n"
        for step in self.steps:
            text += f"\t{str(step)}\n"
        return text