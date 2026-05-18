from job import Job
from step import Step
from helpers import fatal_error, execute


JOBS_TAG = "jobs"
STEPS_TAG = "steps"
JOB_NAME_TAG = "job"
SCRIPT_TAG = "script"
TASK_TAG = "task"
INPUTS_TAG = "inputs"
CONTAINER_TAG = "container"
IMAGE_TAG = "image"

DOCKER_COMMAND_TAG = "command"
DOCKER_IMAGE_TAG = "imageName"
DOCKER_FILE_TAG = "dockerfile"
DOCKER_TAGS_TAG = "tags"


class Pipeline:
    def __init__(self, configuration):
        self.jobs = []
        if not configuration:
            fatal_error("Pipeline configuration is empty!")
        self.configuration = configuration
        self.context = None

    def __process_job_step(self, step, job):
        pass

    @staticmethod
    def __process_docker_build(input_file, name):
        cmd = f"docker build -t {name} -f {input_file} ."
        return execute(cmd, verbose=True, no_fatal=True)


    def configure(self):
        c = self.configuration
        if JOBS_TAG not in c:
            return False

        jobs = c[JOBS_TAG]
        for item in jobs:
            number = 0
            name = item[JOB_NAME_TAG]
            context = None
            if CONTAINER_TAG in item:
                if IMAGE_TAG in item[CONTAINER_TAG]:
                    context = item[CONTAINER_TAG][IMAGE_TAG]

            job = Job(name, context)

            steps = item[STEPS_TAG]
            for step in steps:
                if SCRIPT_TAG in step:
                    # we are only interested in script tags
                    data = step[SCRIPT_TAG]
                    job_step = Step(f"job_{name}_step_{number}", data)
                    job.add_step(job_step)
                elif TASK_TAG in step and INPUTS_TAG in step:
                    task = step[TASK_TAG]
                    data = step[INPUTS_TAG]
                    if task == "Docker@2":
                        if data[DOCKER_COMMAND_TAG] == "build":
                            dockerfile = data[DOCKER_FILE_TAG]
                            tag = data[DOCKER_TAGS_TAG]
                            if not self.__process_docker_build(dockerfile, tag):
                                fatal_error(f"Dockerfile {dockerfile} could not be build!")

            self.jobs.append(job)

        return True

    def execute(self):
        for job in self.jobs:
            print(f"Executing job {job.name}...")

            if not job.run_steps():
                print(f"Job {job.name} failed")
                return False

        return True
