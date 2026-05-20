import configparser


MAIN_SECTION = "main"
DOCKERFILE_KEY = "dockerfile"
NAME_KEY = "name"


class Config:
    def __init__(self, config_file):
        c = configparser.ConfigParser()
        c.read(config_file)
        main_section = c[MAIN_SECTION]
        self.dockerfile = main_section[DOCKERFILE_KEY] or ""
        self.name = main_section[NAME_KEY] or "autobuild"
