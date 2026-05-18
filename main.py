#!/bin/env python

import yaml
import os

import helpers
from pipeline import Pipeline


VERSION = 1


PIPELINE_FILENAME = "azure-pipelines.yml"


def main():
    if not os.path.exists(PIPELINE_FILENAME):
        helpers.fatal_error(f"Pipeline file {PIPELINE_FILENAME} not found in pwd")

    data = yaml.load(open(PIPELINE_FILENAME), Loader=yaml.FullLoader)
    pipeline = Pipeline(data)

    if not pipeline.configure():
        helpers.fatal_error("Pipeline setup failed!")

    if not pipeline.execute():
        helpers.fatal_error("Pipeline execute failed!")

    print("\npipeline okay!\n")




if __name__ == "__main__":
    main()
