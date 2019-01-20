import asyncio
import websockets
import threading
import queue

messages = queue.Queue()
uri = "ws://trevorlaptop.dyn.wpi.edu/websocket"
t = 0

async def receiver():
    async with websockets.connect(uri) as websocket:
        while True:
            messages.put(await websocket.recv())

def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(receiver())

def run_web_socket():
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=loop_in_thread, args=(loop,))
    t.start()

def exit_web_socket():
    t.exit()
    


######################################### ROBAIRE PUT THIS IN THE GAME
#run_web_socket()
# while True:
#     if not messages.empty():
#         print(messages.get())

###########################################
