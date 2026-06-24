import configparser

import helpers


DEFAULT_INTERACTIVE_SHELLL = "/bin/sh"


MAIN_SECTION = "main"
DEFAULT_KEY = "default"
DOCKERFILE_KEY = "dockerfile"
PIPELINEFILE_KEY = "pipeline"
NAME_KEY = "name"
INTERACTIVE_SHELL_KEY = "interactive_shell"

PROFILE_MANDATORY_KEYS = (DOCKERFILE_KEY, PIPELINEFILE_KEY)


class Profile:
    def __init__(self, name, dockerfile, pipeline, interactive_shell):
        self.name = name
        self.dockerfile = dockerfile
        self.pipeline = pipeline
        self.interactive_shell = interactive_shell


class Config:
    def __init__(self, config_file):
        self.__profiles = []
        c = configparser.ConfigParser()
        c.read(config_file)
        main_section = c[MAIN_SECTION]
        self.default = main_section[DEFAULT_KEY]

        for section in c.sections():
            if section == MAIN_SECTION:
                continue

            section_object = c[section]
            if helpers.config_section_has_all_keys(section_object, PROFILE_MANDATORY_KEYS):
                dockerfile = section_object[DOCKERFILE_KEY]
                pipeline = section_object[PIPELINEFILE_KEY]
                if INTERACTIVE_SHELL_KEY in section_object:
                    shell = section_object[INTERACTIVE_SHELL_KEY]
                else:
                    shell = DEFAULT_INTERACTIVE_SHELLL

                profile = Profile(section, dockerfile, pipeline, shell)
                self.__profiles.append(profile)
                print(f" added profile {section}")
            else:
                print(f"WARNING: Section {section} does not have all mandatory keys, ignoring...")

    def get_profile(self, profile) -> Profile:
        for item in self.__profiles:
            if item.name == profile:
                return item

        return None

    def get_default(self):
        return self.get_profile(self.default)
