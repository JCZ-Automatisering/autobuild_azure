import re

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
NAME_TAG = "name"
VARIABLES_TAG = "variables"


DOCKER_COMMAND_TAG = "command"
DOCKER_IMAGE_TAG = "imageName"
DOCKER_FILE_TAG = "dockerfile"
DOCKER_TAGS_TAG = "tags"


_VAR_RE = re.compile(r"\$\(([A-Za-z_][A-Za-z0-9_.-]*)\)")


class Pipeline:
    def __init__(self, configuration):
        self.jobs = []
        if not configuration:
            fatal_error("Pipeline configuration is empty!")
        self.configuration = configuration
        self.context = None
        self.variables = {}
        self.__process_variables()

    def __process_variables(self):
        if VARIABLES_TAG not in self.configuration:
            return      # no variables

        p_vars = self.configuration[VARIABLES_TAG]
        for item in p_vars:
            self.__process_variable(item, p_vars[item])

    def __expand(self, text):
        def _repl(m: re.Match) -> str:
            name = m.group(1)
            try:
                return str(self.variables[name])
            except KeyError:
                raise KeyError(f"undefined variable $({name})") from None

        return _VAR_RE.sub(_repl, text)

    def __process_variable(self, name, value):
        final_value = self.__expand(value)
        self.variables[name] = final_value

    def __process_job_step(self, step, job):
        pass

    @staticmethod
    def __process_docker_build(input_file, name):
        cmd = f"docker build -t {name} -f {input_file} ."
        return execute(cmd, verbose=True, no_fatal=True)

    def configure_job_steps(self, job, steps):
        number = 1
        for step in steps:
            if NAME_TAG in step:
                step_name = step[NAME_TAG]
            else:
                step_name = f"job_{job.name}_step_{number}"

            number += 1

            if SCRIPT_TAG in step:
                # we are only interested in script tags
                data = step[SCRIPT_TAG]
                final_data = self.__expand(data)
                job_step = Step(step_name, final_data)
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

    def configure_with_jobs(self, jobs):
        for item in jobs:
            name = item[JOB_NAME_TAG]
            context = None
            if CONTAINER_TAG in item:
                if IMAGE_TAG in item[CONTAINER_TAG]:
                    context = item[CONTAINER_TAG][IMAGE_TAG]

            job = Job(name, context)

            self.configure_job_steps(job, item[STEPS_TAG])


        return True

    def configure(self):
        c = self.configuration
        if JOBS_TAG in c:
            return self.configure_with_jobs(c[JOBS_TAG])

        job = Job("default", None)  # todo - None -> take from pipeline
        self.configure_job_steps(job, c[STEPS_TAG])
        return True

    def execute(self, context=None):
        for job in self.jobs:
            if context:
                job.context = context
            print(f"Executing job {job.name} (context={context.name})...")

            if not job.run_steps():
                print(f"Job {job.name} failed")
                return False

        return True
