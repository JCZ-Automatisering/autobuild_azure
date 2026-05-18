import os
from sys import intern
from helpers import execute


class Docker:
    def __init__(self, name):
        self.name = name
        self.volumes = ["/etc/passwd", "/etc/group", "/tmp"]
        self.interactive = False

    def start(self):
        pass

    def stop(self):
        pass

    def __build_volumes_args(self):
        output = ""
        for item in self.volumes:
            output += f"-v {item}:{item} "

        cur_dir = os.path.abspath(os.curdir)
        output += f"-v {cur_dir}:{cur_dir} -w {cur_dir}"

        return output

    def __build_docker_cmd(self, cmd, image):
        if self.interactive:
            interactive_flag = "-it"
        else:
            interactive_flag = ""

        volumes = self.__build_volumes_args()

        cmd = f"docker run {interactive_flag} --rm {volumes} {image} {cmd}"
        return cmd

    def run_once(self, cmd):
        final_cmd = self.__build_docker_cmd(cmd, self.name)
        execute(final_cmd, verbose=True)
