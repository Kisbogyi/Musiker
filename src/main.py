#!/usr/bin/env python3
import mpv
from threading import Thread

class Queue:
    def __init__(self):
        self.queue = []

    def add(self, item):
        self.queue.append(item)

    def remove(self, index):
        self.queue.remove( index)

    def clear(self):
        self.queue.clear()

    def pop(self):
        return self.queue.pop(0)

    def __repr__(self) -> str:
        return self.queue.__repr__()

    def len(self):
        return len(self.queue)

class Player:
    paused: bool = True
    def __init__(self) -> None:
        self.player = mpv.MPV(ytdl=True, input_default_bindings=True, input_vo_keyboard=True, vid=False) 
        self.que = Queue()

    async def play(self):
        self.paused = False
        self.player_thread = Thread(target=self.play2)
        self.player_thread.start()

    def play2(self):
        while self.que.len() >= 0 and not self.paused:
            print(self.paused)
            print(self.que)
            self.player.play(self.que.pop())
            self.player.wait_for_playback()

    async def add_to_que(self, url):
        self.que.add(url)

    def stop(self):
        self.player.stop()
        self.paused = True
