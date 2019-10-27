# Dockerserve
Dockerserve is a simple, lightweight Python script for serving a directory in an Nginx Docker container. It is intended as a development tool, similar to XAMPP or your IDE's built-in live server.

## Prerequisites
- Python 3
- Docker

## Installation
1. Download the `dockerserve.py` script and save it to any location
2. (optional) Create a bash alias for `/path/to/dockerserve.py`

## Usage
_Note: we assume that you have added an alias called `dockerserve` for `/path/to/dockerserve.py`._

To use Dockerserve, `cd` into the directory you want to serve as a web root.
- `dockerserve`: print the help
- `dockerserve start <port>`: serve this directory as a web root (make sure that no other container or service is currently using `port`, otherwise, Docker won't be able to start the container)
- `dockerserve stop`: stop serving this directory

## Limitations
Dockerserve does not inject any code into your source files and thus, does not support automatic live reloading on file changes.

## Disclaimer
This project is not affiliated with either Docker or Nginx.

## License
[GNU GPL v3.0](https://github.com/SilasBerger/dockerserve/blob/master/LICENSE)
