import os
import gi
import asyncio
import logging
import sys
import readchar
import re

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
        self.regex = re.compile('[0-9]+', re.IGNORECASE)

        if "-d" in sys.argv:
            os.putenv('GST_DEBUG_DUMP_DOT_DIR',path+'/dot')
            os.putenv('GST_DEBUG', '1')
            logging.basicConfig(level = logging.INFO)

        Gst.init(None)

    async def fetchData(self):
        self.data = self.firebaseDatabase.getData()

    async def fetchFiles(self):
        self.firebaseDatabase.getSongsFiles()

    def startReading(self):
        print("Song code:")
        bufferString = readchar.readkey()
        bufferString += readchar.readkey()

        if bufferString.startswith("0"):
            bufferString = bufferString[1:]

        self.processBuffer(bufferString)

    def processBuffer(self, inputString):
        if inputString == '**':
            print("Updating database...")
            self.updateData()
        elif inputString == '--' :
            print("Closing application...")
            return
        elif self.regex.match(inputString):
            print("Preparing to play a song: "+inputString)
            self.playSong(inputString)

        self.startReading()

    def playSong(self, songKey):
        try:
            song_name = main.data['songs'][songKey]
            song_path = main.songsFolder+u'/'+song_name
            if Path(main.songsFolder+u'/'+song_name).exists():
                logging.debug("Path: {}".format(song_path))
                mediaPlayer = MediaPlayer()
                mediaPlayer.play_sound(song_path)
        except:
            pass

    def updateData(self):
        try:
            self.loop.run_until_complete(main.fetchData())
            self.loop.run_until_complete(main.fetchFiles())
        except:
            pass


if __name__ == '__main__':

    main = Main()
    main.updateData()

    if main.data:
        logging.debug("Data: {}".format(main.data))
        main.startReading()

    else:
        logging.error(u'Data is empty')


