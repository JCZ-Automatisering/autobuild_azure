import configparser
import os.path

import helpers


DEFAULT_INTERACTIVE_SHELLL = "/bin/sh"


MAIN_SECTION = "main"
DEFAULT_KEY = "default"
DOCKERFILE_KEY = "dockerfile"
PIPELINEFILE_KEY = "pipeline"
NAME_KEY = "name"
INTERACTIVE_SHELL_KEY = "interactive_shell"
MOUNT_HOME_KEY = "mount_home"

PROFILE_MANDATORY_KEYS = (DOCKERFILE_KEY, PIPELINEFILE_KEY)


class Profile:
    def __init__(self, name, dockerfile, pipeline, interactive_shell, mount_home):
        self.name = name
        self.dockerfile = dockerfile
        self.pipeline = pipeline
        self.interactive_shell = interactive_shell
        self.mount_home = mount_home


class Config:
    def __init__(self, config_file, skip_file):
        self.__profiles = []
        c = configparser.ConfigParser()
        c.read(config_file)
        main_section = c[MAIN_SECTION]
        self.default = main_section[DEFAULT_KEY]

        self.__handle_autoskip(skip_file)

        for section in c.sections():
            if section == MAIN_SECTION:
                continue

            section_object = c[section]
            if helpers.config_section_has_all_keys(section_object, PROFILE_MANDATORY_KEYS):
                dockerfile = section_object[DOCKERFILE_KEY]
                pipeline = section_object[PIPELINEFILE_KEY]
                shell = self.__get_key_value(section_object, INTERACTIVE_SHELL_KEY, DEFAULT_INTERACTIVE_SHELLL)
                mount_home = self.__get_key_value_boolean(section_object, MOUNT_HOME_KEY, False)

                profile = Profile(section, dockerfile, pipeline, shell, mount_home)
                self.__profiles.append(profile)
                print(f" added profile {section}")
            else:
                print(f"WARNING: Section {section} does not have all mandatory keys, ignoring...")

    @staticmethod
    def __handle_autoskip(file):
        if not os.path.exists(file):
            return

        with open(file) as f:
            print(f"as requested (see {file}), skipping steps:")
            skip_list = ""
            for line in f.readlines():
                line = line.strip()
                skip_list = f"{skip_list},{line}"
                print(f"   step: {line}")

            if skip_list:
                result = skip_list[1:]
                os.environ["SKIP"] = result

            print("")

    @staticmethod
    def __get_key_value(section_object, key, default_value=None):
        if key in section_object:
            return section_object[key]
        return default_value

    @staticmethod
    def __get_key_value_boolean(action_object, key, default_value=False):
        value = Config.__get_key_value(action_object, key, default_value)
        if type(value) == str:
            return helpers.string_to_boolean(value)
        return value


    def get_profile(self, profile) -> Profile:
        for item in self.__profiles:
            if item.name == profile:
                return item

        return None

    def get_default(self):
        return self.get_profile(self.default)
