import os
import gi
import asyncio
import logging
import sys


gi.require_version('Gst', '1.0')
from gi.repository import Gst
from gi.repository import GLib
from gst import MediaPlayer
from firebase import FirebaseManager
from pathlib import Path

class Main(object):

    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.loop = asyncio.get_event_loop()
        self.songsFolder = path+'/songs'
        self.keysFolder = path+'/Keys'
        self.firebaseDatabase = FirebaseManager(self.songsFolder, self.keysFolder)
        self.data = dict()

        if "-d" in sys.argv:
            os.putenv('GST_DEBUG_DUMP_DOT_DIR',path+'/dot')
            os.putenv('GST_DEBUG', '1')
            logging.basicConfig(level = logging.INFO)

        Gst.init(None)

    async def fetchData(self):
        self.data = self.firebaseDatabase.getData()

    async def fetchFiles(self):
        self.firebaseDatabase.getSongsFiles()

    def processInput(self):
        while True:
            try:
                console_input = input("Song code: ")
                if console_input == "-":
                    break
                elif console_input == "*":
                    self.updateData()
                    continue

                song_name = main.data['songs'][console_input]
                song_path = main.songsFolder+u'/'+song_name
                if Path(main.songsFolder+u'/'+song_name).exists():
                    logging.debug("Path: {}".format(song_path))
                    mediaPlayer = MediaPlayer()
                    mediaPlayer.play_sound(song_path)
            except:
                continue

    def updateData(self):
        self.loop.run_until_complete(main.fetchData())
        self.loop.run_until_complete(main.fetchFiles())


if __name__ == '__main__':

    main = Main()
    main.updateData()

    if main.data:
        logging.debug("Data: {}".format(main.data))
        main.processInput()

    else:
        logging.error(u'Data is empty')


