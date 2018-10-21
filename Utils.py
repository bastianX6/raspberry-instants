from datetime import datetime
import platform

def getDateTimeString():
    now = datetime.now()
    return "{}{}{}_{}{}{}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)

def isLinuxOS():
    platformName = platform.system()
    return platformName.startswith('Linux')
