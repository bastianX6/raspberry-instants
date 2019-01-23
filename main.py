import os
import gi
import asyncio
import logging
import sys
import re

gi.require_version('Gst', '1.0')
from gi.repository import Gst
from gi.repository import GLib
from MediaPlayer import MediaPlayer
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
        self.songsArray = []
        self.regex = re.compile('[0-9]+', re.IGNORECASE)

        if "-d" in sys.argv:
            os.putenv('GST_DEBUG_DUMP_DOT_DIR',path+'/dot')
            os.putenv('GST_DEBUG', '3')
            logging.basicConfig(level = logging.INFO)

        Gst.init(None)

    async def fetchData(self):
        self.data = self.firebaseDatabase.getData()

    async def fetchFiles(self):
        self.firebaseDatabase.getSongsFiles()

    def readInput(self):
        inputString = input("Song code: ")

        if inputString == '*':
            print("Updating database...")
            self.updateData()
        elif inputString == '.':
            print("stopping all sounds...")
            self.stopAllSongs()
        elif inputString == '-' :
            print("Closing application...")
            return
        elif self.regex.match(inputString):
            print("Preparing to play a song: "+inputString)
            self.playSong(inputString)

        self.readInput()

    def playSong(self, songKey):
        try:
            songName = self.data['songs'][songKey]
            songPath = self.songsFolder+'/'+songName
            if Path(songPath).exists():
                self.playSongWithPath(songPath)
        except:
            pass

    def playSongWithPath(self, songPath):
        logging.debug("Path: {}".format(songPath))
        mediaPlayer = MediaPlayer()
        mediaPlayer.playSound(songPath)
        self.songsArray.append(mediaPlayer)

    def updateData(self):
        try:
            self.loop.run_until_complete(main.fetchData())
            self.loop.run_until_complete(main.fetchFiles())
        except:
            pass

    def stopAllSongs(self):
        for mediaPlayer in self.songsArray:
            logging.debug("Current state for pipeline: {}".format(mediaPlayer.getState()))
            mediaPlayer.stopSound()
        self.songsArray.clear()

if __name__ == '__main__':

    main = Main()
    main.updateData()

    if main.data:
        logging.debug("Data: {}".format(main.data))
        main.playSongWithPath(main.songsFolder+'/init.mp3')
        main.readInput()

    else:
        logging.error('Data is empty')


