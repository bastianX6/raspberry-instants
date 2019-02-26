import gi
import logging
import Utils
import time

gi.require_version('Gst', '1.0')
from gi.repository import Gst
from gst_element_names import GstElementNames
from MediaPlayer import MediaPlayer

class ClockMediaPlayer(object):

    def __init__(self, fileLocationArray):
        self.mediaPlayers = []
        for fileLocation in fileLocationArray:
            mediaPlayer = MediaPlayer(fileLocation)
            self.mediaPlayers.append(mediaPlayer)

    def cleanup(self):
        for mediaPlayer in self.mediaPlayers:
            mediaPlayer.cleanup()

    def playSound(self):
        for mediaPlayer in self.mediaPlayers:
            mediaPlayer.playSound()
            time.sleep(1)

    def stopSound(self):
        for mediaPlayer in self.mediaPlayers:
            mediaPlayer.stopSound()