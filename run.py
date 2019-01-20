import asyncio
import websockets
import threading
import queue

import kinect
import pygame

messages = queue.Queue()

uri = "ws://kinectmeme.com/websocket"


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



__main__ = "Kinect Tracking"

game = kinect.Game(1920, 1080, "Dumb Kinect Game")
pygame.time.delay(3000)
run_web_socket()
game.game_loop()

######################################### ROBAIRE PUT THIS IN THE GAME
#run_web_socket()
while True:
    if not messages.empty():
        print(messages.get())

###########################################
