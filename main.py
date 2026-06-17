#!/bin/env python

import yaml
import os
from config import Config
import sys

import helpers
from pipeline import Pipeline
from docker import Docker


VERSION = 2


PIPELINE_FILENAME = os.getenv("PIPELINE", "azure-pipelines.yml")
AUTOBUILD_CONFIG = "autobuild.ini"





def main():
    check_files = {
        PIPELINE_FILENAME: f"Pipeline file {PIPELINE_FILENAME} not found in pwd",
        AUTOBUILD_CONFIG: f"Autobuild configuration file {AUTOBUILD_CONFIG} not found in pwd"
    }
    for item in check_files:
        if not os.path.exists(item):
            helpers.fatal_error(check_files[item])

    config = Config(AUTOBUILD_CONFIG)
    if config.dockerfile:
        config.dockerfile = os.getenv("DOCKERFILE", config.dockerfile)
        docker = Docker(config.name)
        docker.build(config.dockerfile)

        if "shell" in sys.argv:
            docker.run_once(config.interactive_shell, interactive=True)
            return
    else:
        docker = None

    data = yaml.load(open(PIPELINE_FILENAME), Loader=yaml.FullLoader)
    pipeline = Pipeline(data)

    if not pipeline.configure():
        helpers.fatal_error("Pipeline setup failed!")

    if not pipeline.execute(config.name if docker else None):
        helpers.fatal_error("Pipeline execute failed!")

    print("\npipeline okay!\n")




if __name__ == "__main__":
    main()
