#!/usr/bin/env python3
import os
from typing import Optional
import mpv
from threading import Thread
import yt_dlp as youtube_dl
from enum import Enum
import uuid

class DownloadStatus(Enum):
    NOT_STARTED = 1
    STARTED = 2
    FINISHED = 3

class Item:
    url = ""
    status = DownloadStatus.NOT_STARTED
    path = ""

    def __init__(self, url) -> None:
         self.url = url

    def get_playable(self):
        if self.status == DownloadStatus.NOT_STARTED:
            return self.url
        else:
            return self.path

class Queue:
    def __init__(self):
        self.queue: list[Item] = []

    def add(self, item):
            self.queue.append(Item(item))

    def remove(self, index):
        self.queue.remove(index)

    def clear(self):
        self.queue.clear()

    def pop_next(self) -> Item:
        return self.queue.pop(0)

    def get_next(self) -> Optional[Item]:
        if len(self.queue) > 0:
            return self.queue[0]
        return None


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
        while self.que.len() >= 1 and not self.paused:
            print(self.paused)
            print(self.que)
            current = self.que.pop_next()
            self.player.play(current.get_playable())
            next = self.que.get_next()
            if next != None:
                self.player_thread = Thread(target=self.cache_song, args=[next])
                self.player_thread.start()
            self.player.wait_for_playback()
            print("start-cleanup")
            self.cleanup(current.path)
            print(self.que.len())

    async def add_to_que(self, url):
        self.que.add(url)

    def stop(self):
        self.player.stop()
        self.paused = True

    def cache_song(self, song: Item):

        path = f"downloaded_{uuid.uuid5}"
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': path
        }

        song.path = f"{path}.part"
        song.status = DownloadStatus.STARTED
        print(song.url)
        print("cache started")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song.url])
        print("download finished")
        song.status = DownloadStatus.FINISHED
        song.path = f"{path}.mp3"


    def cleanup(self, path: str):
        try:
            os.remove(path)
        except:
            pass


