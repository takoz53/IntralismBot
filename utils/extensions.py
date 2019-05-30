import sqlite3
from utils.steamidverify import getSteam64
from threading import Thread


def threaded(fn):
    def wrapper(*args, **kwargs):
        thr = Thread(target=fn, args=args, kwargs=kwargs)
        thr.start()
        return thr

    return wrapper

class Extensions:
    #Class which will only contain Static Methods (and some private Methods)
    #which are needed for multiple files as an extension class
    SQLiteConnection = sqlite3.connect("ProfileLink.db")

    @staticmethod
    def isSteamID(steamID):
        """Checks whether input is proper Steam ID"""
        
        if len(steamID) == 17 and steamID.isdigit():
            return True
        return False

    @staticmethod
    def userExists(discordID):
        """Checks whether current User exists in Database"""
        c = Extensions.SQLiteConnection.cursor()
        c.execute("SELECT steamID FROM profilelink WHERE discordID = ? LIMIT 1", (discordID,))
        result = c.fetchone()
        return result

    @staticmethod
    def convertSteamData(steamID):
        """Converts Input to proper Steam Data if valid"""
        if steamID is None:
            return None
        
        #Is already a Steam ID, so we can return it
        if Extensions.isSteamID(steamID):
            return steamID
        
        #Is a link, so get Steam ID
        newSteamID = getSteam64(steamID)
        if newSteamID is None:
            return None
        return str(newSteamID)

Extensions.convertSteamData = staticmethod(Extensions.convertSteamData)
Extensions.userExists = staticmethod(Extensions.userExists)
Extensions.isSteamID = staticmethod(Extensions.isSteamID)