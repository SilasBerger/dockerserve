#! /usr/bin/python3

import subprocess
import os
import sys
import re


container_name_pattern = re.compile("[a-zA-Z0-9][a-zA-Z0-9_.-]*")


def main():
    if len(sys.argv) == 1:
        print_help()
        return
    command = sys.argv[1]
    if command == "init":
        init()
    elif command == "start":
        start()
    elif command == "stop":
        stop()
    else:
        print_help()
    return 0


def init():
    container_name = None
    while container_name is None:
        new_name = input("Container name: ")
        if container_name_pattern.match(new_name):
            container_name = new_name
        else:
            print("container name must match [a-zA-Z0-9][a-zA-Z0-9_.-]*")
    with open("dockerserve", "w") as dockerserve_file:
        dockerserve_file.truncate()
        dockerserve_file.write(container_name)


def start():
    if len(sys.argv) < 3:
        print_help()
        return
    container_name = _get_container_name()
    pwd = subprocess.check_output(["pwd"]).decode("utf-8").strip()
    subprocess.run(["docker", "container", "run", "--rm", "-d", "--name", container_name,
                    "-v", (pwd + "://usr/share/nginx/html:ro"), "nginx:1.17"])


def stop():
    container_name = _get_container_name()
    subprocess.run(["docker", "container", "stop", container_name])


def _read_dockerserve_file():
    try:
        with open("dockerserve", "r") as dockerserve_file:
            return dockerserve_file.readlines()
    except FileNotFoundError:
        print("Error: dockerserve file missing - run 'dockerserve init'\n")


def _get_container_name():
    pwd = subprocess.check_output(["pwd"]).decode("utf-8").strip()
    sanitized = pwd.replace("/", "-")
    sanitized = sanitized.replace(":", "")
    sanitized = sanitized.replace(" ", "_")
    return "dockerserve" + sanitized


def print_help():
    print("Serve the present working directory in an Nginx Docker container.\n")
    print("Usage:")
    print("\tdockerserve init: initialize this directory for dockerserve")
    print("\tdockerserve start <port>: serve this directory")
    print("\tdockerserve stop: stop serving this directory")
    print("\tdockerserve: print this help")
    print("")


if __name__ == "__main__":
    main()