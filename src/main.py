#!/usr/bin/venv python3

from threading import Thread, Event
import mpv

import yt_dlp


class QuietLogger:
    @staticmethod
    def error(_):
        pass
    @staticmethod
    def warning(_):
        pass
    @staticmethod
    def debug(_):
        pass

def get_urls_from_json(video_data):
    if "entries" in video_data:
        return (True, video_data["entries"][0]["url"])
    return (False, video_data["url"]) 


def get_links(url):
    i: int = 1
    download = True
    while download:
        opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'playlist_items': f'{i}',
            'extractor_retries': 3,
            'quiet': True,
            'logger': QuietLogger
        }

        i += 1
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download = False)
            try:
                playlist, _url = get_urls_from_json(info)
                if not playlist:
                    download = False
                yield _url
            except IndexError:
                return



# https://www.youtube.com/watch?v=YpJAmlnBxoA&list=RDEMBhlpzGCZlXxLMeHLVGJ2lQ&start_radio=1
# https://www.youtube.com/watch?v=txBfhpm1jI0&list=RDEMVI7wjlFbHpB5qeqCapX6gQ&start_radio=1
# https://www.youtube.com/watch?v=mjF1rmSV1dM&list=RDEMh1nfQXGRbitrlSs8fEQK1g&start_radio=1 
# https://www.youtube.com/watch?v=9R-mWbxMN4I&list=PL9fPq3eQfaaBTZWTBe3x17Hz68UqRTDrL

class Player:
    # Playlist contains urls from playlists and videos, play will play them with generator
    # TODO: threads can only be started once
    # skip response elhal
    #push first
    # stop is not pouse with mpv
    playerStarted: Event = Event()
    playlist = []
    def __init__(self):
        self.player =  mpv.MPV(ytdl=True, input_vo_keyboard=True, vid=False)
        def __play():
            while True:
                self.playerStarted.wait()
                if len(self.playlist) == 0:
                    self.playerStarted.clear()
                    continue
                video = self.playlist.pop(0)
                for music in get_links(video):
                    print(f"playing {music}")
                    self.player.play(music)
                    self.player.wait_for_playback()
 

        self.playingThread: Thread = Thread(target=__play)
        self.playingThread.start()

    def play(self):
        self.playerStarted.set()

    def add(self, url):
        self.playlist.append(url)
        self.playerStarted.set()

    def stop(self):
        # TODO: Make mpv pause
        #self.player.keydown()
        #self.player.__setattr__("pause", not self.player.__getattr__("pause"))
        self.player.command("cycle", "pause")

        #self.playerStarted.clear()
        #self.player.stop(keep_playlist=True)

    def skip(self):
        self.player.stop()
        self.play()

    def clear(self):
        self.playlist.clear()

    def set_property(self, name, value):
        """Set the value of property `name`.
        """
