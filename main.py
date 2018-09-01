import os
import gi
import asyncio
import logging


gi.require_version('Gst', '1.0')
from gi.repository import Gst
from gi.repository import GLib
from gst import MediaPlayer
from firebase import FirebaseDatabse
from pathlib import Path

class Main(object):

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.firebaseDatabase = FirebaseDatabse()
        self.data = dict()
        self.currentFolder = os.getcwd()+'/songs'
        os.putenv('GST_DEBUG_DUMP_DOT_DIR',os.getcwd()+'/dot')
        os.putenv('GST_DEBUG', '2')
        logging.basicConfig(level = logging.INFO)

        Gst.init(None)

    async def fetchData(self):
        self.data = self.firebaseDatabase.getData()

    def processInput(self):
        try:
            console_input = input("Song code: ")
            song_name = main.data['songs'][console_input]
            song_path = main.currentFolder+u'/'+song_name
            if Path(main.currentFolder+u'/'+song_name).exists():
                logging.debug("Path: {}".format(song_path))
                mediaPlayer = MediaPlayer()
                mediaPlayer.play_sound(song_path, self.onPlayingEnded)
        except:
            self.processInput()
          

    def onPlayingEnded(self):
        self.processInput()


if __name__ == '__main__':

    main = Main()
    main.loop.run_until_complete(main.fetchData())  

    if main.data:
        logging.debug("Data: {}".format(main.data))
        main.processInput()
        
    else:
        logging.error(u'Data is empty')


