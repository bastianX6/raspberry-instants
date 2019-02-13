import gi
import logging
import Utils

gi.require_version('Gst', '1.0')
from gi.repository import Gst
from gst_element_names import GstElementNames

class MediaPlayer(object):

    def __init__(self, fileLocation):
        self.playBin = Gst.ElementFactory.make("playbin", "playbin")
        self.fileLocation = fileLocation
        self.state = Gst.State.NULL
        if not self.playBin:
            logging.error("Error: could not create playbin for song: %s", self.fileLocation)
        else:
            logging.debug("File path: file://%s", self.fileLocation)
            self.playBin.set_property("uri", "file://"+self.fileLocation)

    def cleanup(self):
        if self.playBin:
            self.playBin.set_state(Gst.State.NULL)
            self.playBin = None

    def playSound(self):
        self.playBin.set_state(Gst.State.PLAYING)
        pass

    def stopSound(self):
        self.playBin.set_state(Gst.State.READY)
        self.cleanup()
        pass