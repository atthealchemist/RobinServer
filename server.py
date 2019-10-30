import sys
import json
import asyncio
import websockets

from websockets.exceptions import ConnectionClosedError


def exit_server(sig, frame):
    print("Exiting...")
    asyncio.get_event_loop().stop()
    sys.exit(0)


async def double_value(websocket, path):
    try:
        async for value in websocket:
            await asyncio.sleep(1)
            print(f"ws get: {value}")
            query = json.loads(value)

            query['Number'] *= 2
            query['Status'] = "OK"

            response = json.dumps(query)         
            await websocket.send(response)
            print(f"ws sent: {response}")
    except ConnectionClosedError:
        print("connection closed")


def main(*args, **kwargs):

    port = 8765
    if len(args) > 0:
        port = int(args[0])

    start_server = websockets.serve(double_value, "localhost", port)
    print(f"Starting websockets server @ localhost:{port} ")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
