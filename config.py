import configparser


MAIN_SECTION = "main"
DOCKERFILE_KEY = "dockerfile"
NAME_KEY = "name"
INTERACTIVE_SHELL_KEY = "interactive_shell"


class Config:
    def __init__(self, config_file):
        c = configparser.ConfigParser()
        c.read(config_file)
        main_section = c[MAIN_SECTION]
        self.dockerfile = main_section[DOCKERFILE_KEY] or ""
        self.name = main_section[NAME_KEY] or "autobuild"
        self.interactive_shell = main_section[INTERACTIVE_SHELL_KEY] or "/bin/sh"
