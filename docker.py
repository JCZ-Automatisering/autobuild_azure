import os
import tempfile

import helpers
from helpers import execute
from pathlib import Path


class Docker:
    def __init__(self, name, mount_home=False):
        self.name = name
        self.volumes = ["/etc/passwd", "/etc/group", "/tmp"]
        self.interactive = False
        self.__docker_script_obj = tempfile.NamedTemporaryFile()
        self.__docker_script = self.__docker_script_obj.name
        self.volumes.append(self.__docker_script)
        self.mount_home = mount_home

    def build(self, dockerfile):
        cmd = f"docker build -t {self.name} -f {dockerfile} ."
        execute(cmd, verbose=True)

    def start(self):
        pass

    def stop(self):
        pass

    def __build_volumes_args(self):
        output = ""
        for item in self.volumes:
            output += f"-v {item}:{item} "

        if self.mount_home:
            home_dir = Path.home()
            output += f" -v {home_dir}:{home_dir} "

        cur_dir = os.path.abspath(os.curdir)
        output += f"-v {cur_dir}:{cur_dir} -w {cur_dir}"

        return output

    def __build_docker_base(self, image, root=False):
        if self.interactive:
            interactive_flag = "-it"
        else:
            interactive_flag = ""

        volumes = self.__build_volumes_args()

        if root:
            uid = 0
            gid = 0
        else:
            uid = helpers.get_current_user_id()
            gid = helpers.get_current_group_id()

        cmd = f"docker run {interactive_flag} --hostname {self.name} --rm --user {uid}:{gid} {volumes} {image}"
        return cmd

    def run_once(self, cmd, root=False, interactive=False):
        if interactive:
            self.interactive = True
        else:
            self.interactive = False

        final_cmd = self.__build_docker_base(image=self.name, root=root)

        script_content = f"#!/bin/sh\n\n{cmd}\n"
        open(self.__docker_script, "w").write(script_content)

        final_cmd += f" /bin/sh {self.__docker_script}"

        print(f"\ndocker step script: {cmd}")
        return execute(final_cmd, verbose=True, no_fatal=True)
