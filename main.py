#!/bin/env python

import yaml
import os

from config import Config
import sys

import helpers
from pipeline import Pipeline
from docker import Docker
from environment import Environment


VERSION = 10


AUTOBUILD_CONFIG = "autobuild.ini"
AUTOBUILD_AUTOSKIP_FILE = ".autobuild_auto_skip"
AUTOBUILD_ENVIRONMENT_FILE = ".autobuild_environment"
SHELL_KEY = "shell"


def main():
    print(f"Autobuild azure, version {VERSION}\n")
    check_files = {
        AUTOBUILD_CONFIG: f"Autobuild configuration file {AUTOBUILD_CONFIG} not found in pwd"
    }
    for item in check_files:
        if not os.path.exists(item):
            helpers.fatal_error(check_files[item])

    config = Config(AUTOBUILD_CONFIG, AUTOBUILD_AUTOSKIP_FILE)
    profile = config.get_default()
    if len(sys.argv) > 1:
        profile_name = sys.argv[1]
        if not profile_name == SHELL_KEY:
            profile = config.get_profile(profile_name)

    if not profile:
        helpers.fatal_error(f"Could not load profile!")

    environment = Environment(AUTOBUILD_ENVIRONMENT_FILE)

    # todo: make docker optional again?
    docker = Docker(profile.name, profile.mount_home, environment.environment)
    docker.build(profile.dockerfile)
    if SHELL_KEY in sys.argv:
        docker.run_once(profile.interactive_shell, interactive=True)
        return
    # else:
    #     docker = None

    data = yaml.load(open(profile.pipeline), Loader=yaml.FullLoader)
    pipeline = Pipeline(data)

    if not pipeline.configure():
        helpers.fatal_error("Pipeline setup failed!")

    if not pipeline.execute(docker):
        helpers.fatal_error("Pipeline execute failed!")

    print("\npipeline okay!\n")




if __name__ == "__main__":
    main()
