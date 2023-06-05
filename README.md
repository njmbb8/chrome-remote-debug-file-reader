# Chrome Remote Debug Filesystem Explorer

Uses Chrome's remote debugger to explore the file system

## Installation

You should be able to just run the script using Python3, but you'll need the following libraries if not already installed:

1. sys
2. websockets
3. argparse
4. requests
5. asyncio
6. json
7. itertools
8. pandas


## Usage

Read files accessible to a user running Chrome Remote Debugger [-h] [-i IP] [-p PORT]
[-f FILE] [-s]

options:

  -h, --help            show this help message and exit

  -i IP, --ip IP        IP Address remote debugger is listening on

  -p PORT, --port PORT  Port remote debugger is listening on

  -f FILE, --file FILE  File to steal

  -s, --secure          Use https

## When is this useful?

If(for some reason) you find a remote debugger port that is exposed externally, you can explore the filesystem as the user running the debugger. Chances are, you've already exploited a machine if you have access to a remote debugger, if that is the case, you can use this tool to explore the filesystem and gain read access to the same files and directories that the user running chrome does.

## License

[MIT](https://choosealicense.com/licenses/mit/)
