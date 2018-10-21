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
        self.loop = asyncio.get_event_loop()
        self.songsFolder = os.getcwd()+'/songs'
        self.firebaseDatabase = FirebaseManager(self.songsFolder)
        self.data = dict()

        if "-d" in sys.argv:
            os.putenv('GST_DEBUG_DUMP_DOT_DIR',os.getcwd()+'/dot')
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

                song_name = main.data['songs'][console_input]
                song_path = main.songsFolder+u'/'+song_name
                if Path(main.songsFolder+u'/'+song_name).exists():
                    logging.debug("Path: {}".format(song_path))
                    mediaPlayer = MediaPlayer()
                    mediaPlayer.play_sound(song_path)
            except:
                continue


if __name__ == '__main__':

    main = Main()
    main.loop.run_until_complete(main.fetchData())
    main.loop.run_until_complete(main.fetchFiles())

    if main.data:
        logging.debug("Data: {}".format(main.data))
        main.processInput()

    else:
        logging.error(u'Data is empty')

