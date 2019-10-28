import asyncio
import websockets

from websockets.exceptions import ConnectionClosedError

import sys
import signal


def exit_server(sig, frame):
    print("Exiting...")
    asyncio.get_event_loop().stop()
    sys.exit(0)


async def double_value(websocket, path):
    try:
        async for value in websocket:
            await asyncio.sleep(1)
            print(f"ws get: {value}")
            if value.isdigit():
                value = int(value) * 2
                await websocket.send(str(value))
                print(f"ws sent: {value}")
    except ConnectionClosedError:
        print("connection closed")


def main(*args, **kwargs):

    signal.signal(signal.SIGINT, exit_server)

    port = 8765
    if len(args) > 0:
        port = int(args[0])

    start_server = websockets.serve(double_value, "localhost", port)
    print(f"Starting websockets server @ localhost:{port} ")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
