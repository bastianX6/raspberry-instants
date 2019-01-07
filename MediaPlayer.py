import gi
import logging
import asyncio
import Utils

gi.require_version('Gst', '1.0')
from gi.repository import Gst
from gst_element_names import GstElementNames

class MediaPlayer(object):

    def __init__(self):
        '''
        Constructor
        '''
        self.element_list = dict()
        self.element_tuple_list = []
        self.binContainer = Gst.Bin()
        self.pipeline = Gst.Pipeline()
        self.bus = self.pipeline.get_bus()
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__on_message)
        self.bus.connect('sync-message::eos', self.__on_eos)
        self.bus.connect('sync-message::error', self.__on_error)
        self.pipeline.add(self.binContainer)
        self.dateTime = Utils.getDateTimeString()

    def playSound(self, fileLocation):
        self.__create_bin__()
        self.__set_property__("filesrc", "location", fileLocation)
        self.__set_property__("filesrc", "stop-index", 0)
        self.pipeline.set_state(Gst.State.PLAYING)

    def stopSound(self):
        self.__destroy_bin__()

    def getState(self):
        return self.parse_state(self.pipeline.current_state)
    # private methods

    # Create and link pipeline elements
    def __create_bin__(self):
        '''
        Creates Gstreamer elements and add them to a Bin. Next, the elements are linked and a observer is configurated.

        Linked elements:

        | filesrc (src) | --> | (sink) decodebin (src) |

        Unlinked elements:

        | (sink) audioconvert (src) |

        | (sink) autoaudiosink |

        '''
        # Create elements
        self.__add_element__(GstElementNames.audioconvert, "audioconvert")
        if Utils.isLinuxOS():
            self.__add_element__(GstElementNames.pulsekink, "audiosink")
        else:
            self.__add_element__(GstElementNames.autoaudiosink, "audiosink")

        self.__add_element__(GstElementNames.multifilesrc, "filesrc")
        self.__add_element__(GstElementNames.decodebin, "decodebin")

        # link elements and set its properties
        self.__link_elements__("filesrc", "decodebin")
        self.__link_elements__("audioconvert", "audiosink")

        #setup observer
        decodebin = self.element_list["decodebin"]
        decodebin.connect("pad-added", self.__on_pad_added_decodebin__)

    def __add_element__(self,factory_name,element_name):
        element = Gst.ElementFactory.make(factory_name,None)
        self.element_list[element_name] = element

        #Add to bin
        self.binContainer.add(element)
        return True

    def __link_elements__(self,source_name,dest_name):
        source = self.element_list[source_name]
        dest = self.element_list[dest_name]
        source.link(dest)

        #Add to tuple list
        the_tuple = (source,dest)
        self.element_tuple_list.append(the_tuple)

    def __set_property__(self,element_name,the_property,value):
        element = self.element_list[element_name]
        element.set_property(the_property,value)

    def __on_pad_added_decodebin__(self, element, pad):
        '''
        Called when decodebin element receives data. This method
        links decodebin with audioconvert and also links audioconvert with autoaudiosink.

        Before this method:

        | filesrc (src) | --> | (sink) decodebin (src) |

        After:

        | filesrc (src) | --> | (sink) decodebin (src) | --> | (sink) audioconvert (src) | --> | (sink) autoaudiosink |

        '''
        #link to audioconvert element
        audioconvert = self.element_list["audioconvert"]
        pad_audioconvert = audioconvert.get_static_pad("sink")
        pad.link(pad_audioconvert)
        self.__link_elements__("audioconvert", "audiosink")
        Gst.debug_bin_to_dot_file (self.pipeline,Gst.DebugGraphDetails.ALL, "pipeline_created_"+self.dateTime)

    # Destroy and unlink pipeline elements
    def __destroy_bin__(self):
        keys = list(self.element_list.keys())
        for key in keys:
            self.__remove_element__(key)

        Gst.debug_bin_to_dot_file (self.pipeline,Gst.DebugGraphDetails.ALL, "pipeline_destroyed_"+self.dateTime)

    def __remove_element__(self,element_name):
        element = self.element_list[element_name]
        self.element_list.pop(element_name)

        self.destroy_element_links(element)

        #Remove from bin
        self.binContainer.remove(element)

    def destroy_element_links(self,element):
        for t in self.element_tuple_list:
            source = t[0]
            dest = t[1]

            if source == element or dest == element:
                source.unlink(dest)
                self.element_tuple_list.remove(t)

    # Pipeline signals
    def __on_message(self, bus, msg):
        if msg.type == Gst.MessageType.STATE_CHANGED:
            states = msg.parse_state_changed()
            logging.debug('Old State: %s | New state: %s | State pending: %s', self.parse_state(states[0]), self.parse_state(states[1]), self.parse_state(states[2]))

        elif msg.type == Gst.MessageType.STREAM_STATUS:
            stream_status = msg.parse_stream_status()
            logging.debug('Stream Status: %s',stream_status[0])
            logging.debug('Element: %s',stream_status[1])

        elif msg.type == Gst.MessageType.WARNING:
            warning = msg.parse_warning()
            logging.warning('Error: %s', warning[0])
            logging.warning('Details: %s', warning[1])

        elif msg.type == Gst.MessageType.TAG:
            logging.debug('Tag: %s',msg.parse_tag().to_string())

        elif msg.type == Gst.MessageType.EOS:
            logging.debug("Message: EOS")
            self.stopSound()

        else:
            logging.debug("Message: %s",msg.type)

    def __on_eos(self, bus, msg):
        self.__destroy_bin__()

    def parse_state(self,gst_state):
        state = ""

        if gst_state == Gst.State.VOID_PENDING:
            state = "VOID_PENDING"

        elif gst_state == Gst.State.NULL:
            state = "NULL"

        elif gst_state == Gst.State.READY:
            state = "READY"

        elif gst_state == Gst.State.PAUSED:
            state = "PAUSED"

        elif gst_state == Gst.State.PLAYING:
            state = "PLAYING"

        return state

    def __on_error(self, bus, msg):
        logging.debug('on_error(): %s', msg.parse_error())
