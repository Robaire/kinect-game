import asyncio
import websockets
import threading
import queue

q = queue.Queue()


uri = "ws://localhost:8080/websocket"


async def receiver():
    async with websockets.connect(uri) as websocket:
        while True:
            q.put(await websocket.recv())


def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(receiver())


def run_web_socket():
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=loop_in_thread, args=(loop,))
    t.start()


######################################### ROBAIRE PUT THIS IN THE GAME
run_web_socket()
while True:
    if not q.empty():
        print(q.get())

###########################################
