#! /usr/bin/python3

import subprocess
import sys
import re


DEFAULT_PORT = "8080"


def main():
    if len(sys.argv) == 1:
        print_help()
        return
    command = sys.argv[1]
    if command == "start":
        start()
    elif command == "stop":
        stop()
    elif command == "status":
        status()
    else:
        print_help()
    return 0


def start():
    port = DEFAULT_PORT
    if len(sys.argv) >= 3:
        port = sys.argv[2]
    container_name = _get_container_name()
    pwd = subprocess.check_output(["pwd"]).decode("utf-8").strip()
    subprocess.run(["docker", "container", "run", "--rm", "-d", "--name", container_name, "-p", (port + ":80"),
                    "-v", (pwd + "://usr/share/nginx/html:ro"), "nginx:1.17"])


def stop():
    container_name = _get_container_name()
    subprocess.run(["docker", "container", "stop", container_name])


def status():
    container_name = _get_container_name()
    containers = subprocess.check_output(["docker", "container", "ls"]).decode("utf-8").strip().split("\n")
    for line in containers:
        if container_name in line:
            ports_pattern = re.compile("\\d+\\.\\d+\\.\\d+\\.\\d+:(\\d+)->80/tcp")
            port = re.search(ports_pattern, line).group(1)
            print("running (port=" + port + ", container=" + container_name + ")\n")
            return
    print("not running\n")


def _get_container_name():
    pwd = subprocess.check_output(["pwd"]).decode("utf-8").strip()
    sanitized = pwd.replace("/", "-")
    sanitized = sanitized.replace(":", "")
    sanitized = sanitized.replace(" ", "_")
    return "dockerserve" + sanitized


def print_help():
    print("Serve the present working directory in an Nginx Docker container.\n")
    print("Usage:")
    print("\tdockerserve start <port>: serve this directory")
    print("\tdockerserve stop: stop serving this directory")
    print("\tdockerserve: print this help")
    print("")


if __name__ == "__main__":
    main()
