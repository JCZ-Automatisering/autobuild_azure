from job import Job
from step import Step


JOBS_TAG = "jobs"
STEPS_TAG = "steps"
JOB_NAME_TAG = "job"
SCRIPT_TAG = "script"


class Pipeline:
    def __init__(self, configuration):
        self.jobs = []
        self.configuration = configuration
        self.context = None

    def configure(self):
        c = self.configuration
        if JOBS_TAG not in c:
            return False

        jobs = c[JOBS_TAG]
        for item in jobs:
            number = 0
            name = item[JOB_NAME_TAG]
            job = Job(name)

            steps = item[STEPS_TAG]
            for step in steps:
                if SCRIPT_TAG in step:
                    # we are only interested in script tags
                    data = step[SCRIPT_TAG]
                    job_step = Step(f"job_{name}_step_{number}", data)
                    job.add_step(job_step)

            self.jobs.append(job)

        return True

    def execute(self):
        for job in self.jobs:
            print(f"Executing job {job.name}...")

            if not job.run_steps(self.context):
                print(f"Job {job.name} failed")
                return False

        return True
