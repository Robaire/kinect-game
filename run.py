import asyncio
import websockets
import threading
import queue

messages = queue.Queue()
<<<<<<< HEAD
uri = "ws://kinectmeme.com/websocket"
t
=======
uri = "ws://trevorlaptop.dyn.wpi.edu/websocket"
t = 0
>>>>>>> 3bba0f3d0c719aab4f4ade34fd6c0668f9a7cb1d

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
