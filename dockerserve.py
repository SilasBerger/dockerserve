#! /usr/bin/python3

import subprocess
import sys


def main():
    if len(sys.argv) == 1:
        print_help()
        return
    command = sys.argv[1]
    if command == "start":
        start()
    elif command == "stop":
        stop()
    else:
        print_help()
    return 0


def start():
    if len(sys.argv) < 3:
        print_help()
        return
    container_name = _get_container_name()
    pwd = subprocess.check_output(["pwd"]).decode("utf-8").strip()
    port = sys.argv[2]
    subprocess.run(["docker", "container", "run", "--rm", "-d", "--name", container_name, "-p", (port + ":80"),
                    "-v", (pwd + "://usr/share/nginx/html:ro"), "nginx:1.17"])


def stop():
    container_name = _get_container_name()
    subprocess.run(["docker", "container", "stop", container_name])


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
