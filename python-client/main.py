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
from Clock import Clock
from pathlib import Path
from flask import Flask, json, request
from flask_cors import CORS, cross_origin

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
            songName = self.data[songKey]
            songPath = self.songsFolder+'/'+songName
            if Path(songPath).exists():
                self.playSongWithPath(songPath)
        except:
            pass

    def playSongWithPath(self, songPath):
        logging.debug("Path: {}".format(songPath))
        mediaPlayer = MediaPlayer(songPath)
        mediaPlayer.playSound()
        self.songsArray.append(mediaPlayer)

    def updateData(self):
        try:
            self.loop.run_until_complete(soundApp.fetchData())
            self.loop.run_until_complete(soundApp.fetchFiles())
        except Exception as e:
            logging.debug("Exception updating data: {}".format(e))
            pass

    def stopAllSongs(self):
        for mediaPlayer in self.songsArray:
            try:
                mediaPlayer.stopSound()
            except Exception as e:
                logging.debug("Exception stopping sound: {}".format(e))
                pass

        self.songsArray.clear()


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
soundApp = Main()

def emptyResponse():
    return json.dumps("{}"), 204, {}

def jsonResponse(data):
    headers = {
        "Content-Type": "application/json",
    }
    return json.dumps(data), 200, headers

@app.route('/play/<soundID>', methods=['GET'])
@cross_origin()
def play(soundID):
    if soundApp.regex.match(soundID):
        print("Preparing to play a song: "+soundID)
        soundApp.playSong(soundID)
    return emptyResponse()

@app.route('/stop', methods=['GET'])
@cross_origin()
def stop():
    print("stopping all sounds...")
    soundApp.stopAllSongs()
    return emptyResponse()

@app.route('/reload', methods=['GET'])
@cross_origin()
def reload():
    print("Updating database...")
    soundApp.updateData()
    return emptyResponse()

@app.route('/list', methods=['GET'])
@cross_origin()
def list():
    print("Listing songs...")
    return jsonResponse(soundApp.data)

@app.route('/clock', methods=['GET'])
@cross_origin()
def readClock():
    print("playing clock...")
    clock = Clock()
    clockDict = clock.getClockCodes()
    clockMediaPlayer = clock.getClockMediaPlayer(soundApp.data, soundApp.songsFolder)
    soundApp.songsArray.append(clockMediaPlayer)
    clockMediaPlayer.playSound()
    return emptyResponse()

if __name__ == '__main__':
    soundApp.updateData()

    if soundApp.data:
        logging.debug("Data: {}".format(soundApp.data))
        if "--http" in sys.argv[1:]:
            logging.info('Running in http listening mode')
            app.run(debug=True, host='127.0.0.1', port=9090)
        else:
            logging.info('Running in local mode')
            soundApp.playSongWithPath(soundApp.songsFolder+'/init.mp3')
            soundApp.readInput()
    else:
        logging.error('Data is empty')

