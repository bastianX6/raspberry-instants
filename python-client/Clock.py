import datetime
import logging
from ClockMediaPlayer import ClockMediaPlayer

class Clock(object):

    def __init__(self):
        self.hourCode = "161"
        self.minuteCode = "162"
        self.oclockCode = "160"

    def getClockCodes(self):
        now = datetime.datetime.now()
        timeDict = dict()

        if now.minute >0 and now.minute < 10:
            timeDict["minute"] = "10{}".format(now.minute)
        else:
            timeDict["minute"] = "1{}".format(now.minute)

        if now.hour == 0:
            timeDict["hour"] = "100"
        elif now.hour > 0 and now.hour < 10:
            timeDict["hour"] = "10{}".format(now.hour)
        else:
            timeDict["hour"] = "1{}".format(now.hour)

        return timeDict

    def getClockMediaPlayer(self, data, songsFolder):
        clockDict = self.getClockCodes()
        codesArray = []
        logging.info("clockDict: {}".format(clockDict))

        #Add hour
        codesArray.append(clockDict["hour"])
        codesArray.append(self.hourCode)

        if "minute" in clockDict:
            codesArray.append(clockDict["minute"])
            codesArray.append(self.minuteCode)
        else:
            codesArray.append(self.oclockCode)

        fileLocationArray = []
        for code in codesArray:
            songName = data[code]
            songPath = songsFolder+'/'+songName
            fileLocationArray.append(songPath)

        return ClockMediaPlayer(fileLocationArray)
