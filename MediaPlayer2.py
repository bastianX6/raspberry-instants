import gi
import logging
import Utils

gi.require_version('Gst', '1.0')
from gi.repository import Gst
from gst_element_names import GstElementNames

class MediaPlayer2(object):

    def __init__(self, fileLocation):
        self.playBin = Gst.ElementFactory.make("playbin", "playbin")
        self.fileLocation = fileLocation
        self.state = Gst.State.NULL
        if not self.playBin:
            logging.error("Error: could not create playbin for song: %s", self.fileLocation)
        else:
            logging.debug("File path: file://%s", self.fileLocation)
            self.playBin.set_property("uri", "file://"+self.fileLocation)

            bus = self.playBin.get_bus()
            bus.add_signal_watch()
            bus.connect("message::error", self.on_error)
            bus.connect("message::eos", self.on_eos)
            bus.connect("message::state-changed", self.on_state_changed)

    def on_error(self, bus, msg):
        error, debugInfo = msg.parse_error()
        logging.error("Gstreamer error - %s: %s", msg.src.get_name(), error.message)
        print("ERROR:", msg.src.get_name(), ":", error.message)
        if debugInfo:
            logging.debug("Debug info: %s", debugInfo)

    def on_eos(self, bus, msg):
        logging.debug("EOS reached")
        self.playBin.set_state(Gst.State.READY)
        self.cleanup()

    def on_state_changed(self, bus, msg):
        oldState, newState, pendingState = msg.parse_state_changed()
        if not msg.src == self.playBin:
            # not from the playbin, ignore
            return
        self.state = newState
        logging.debug("State changed from {0} to {1}. Pending state: {2}".format(Gst.Element.state_get_name(oldState), Gst.Element.state_get_name(newState), Gst.Element.state_get_name(pendingState)))

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