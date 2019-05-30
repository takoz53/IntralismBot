from utils.rank_scraper import scrape, scrapeTop
import re


class PlayerInfo:
    globalRank = None
    globalMax = None
    countryRank = None
    countryMax = None
    accuracy = None
    misses = None
    steamLink = None
    pictureURL = None
    userName = None
    country = None
    countryFlag = None
    points = None
    
    def __init__(self, steamID = None):
        if not steamID:
            return

        self.from_steam(steamID)

    def from_steam(self, steamID):
        """Gets Player Information and saves them to given values via SteamID."""
        playerInformation = self.getPlayerInfo(steamID)
        self.globalRank = playerInformation[0]
        self.globalMax = playerInformation[1]
        self.countryRank = playerInformation[2]
        self.countryMax = playerInformation[3]
        self.accuracy = playerInformation[4]
        self.misses = playerInformation[5]
        self.userName = playerInformation[6]
        self.pictureURL = playerInformation[7]
        self.steamLink = "http://steamcommunity.com/profiles/" + str(steamID)
        
        return self

    def from_object(self, obj):
        self.globalRank = (obj['rank'])
        self.pictureURL = obj['imagePath']
        self.userName = obj['name'],
        self.accuracy = obj['accuracy'],
        self.misses = obj['misses']
        self.country = obj['country'],
        self.points = obj['point']

        return self


    #If rank between 1 and 10, #ffda44
    #If rank between 11 and 25 #E14FFF
    #If rank between 26 and 100 #EA4137
    #If rank between 101 and 501 #91CCFF
    #If rank between >501 #000
    
    def getColor(self, rank):
        if rank < 10:
            color = 0xFFDA44
        elif 11 <= rank <= 25:
            color = 0xE14FFF
        elif 26 <= rank <= 100:
            color = 0xEA4137
        elif 101 <= rank <= 501:
            color = 0x91CCFF
        elif rank > 501:
            color = 0
        return color

        
    def getRankInfo(self, string):
        """Returns Global / Country ranking information"""
        return re.search(r"^(\w+)?\s?(\w+):\s([0-9]+)\s\/\s([0-9]+)$", string)


    def getUserInfo(self, string):
        """Returns further player informations"""
        return re.search(r"^(\w+)?\s?(\w+):\s([0-9]+\.[0-9]{2})", string)


    def getPlayerInfo(self, SteamID):
        """Function which calls the scraper to scrape newest userdata and save them into a list"""
        stats_list = scrape(SteamID)

        globalInfo = self.getRankInfo(stats_list[0])
        countryInfo = self.getRankInfo(stats_list[1])
        accuracyInfo = self.getUserInfo(stats_list[2])
        
        if not globalInfo:
            raise ValueError("Couldn't fetch Global Info")
            
        if not countryInfo:
            raise ValueError("Couldn't fetch Country Info")
        
        if not accuracyInfo:
            raise ValueError("Couldn't fetch Accuracy Info")

        globalRank = globalInfo.group(3)
        globalMax = globalInfo.group(4)
        countryRank = countryInfo.group(3)
        countryMax = countryInfo.group(4)    
        accuracy = accuracyInfo.group(3)
        
        missInfo = self.getUserInfo(stats_list[3])
        nameInfo = stats_list[4]
        avatarInfo = stats_list[5]

        if missInfo:
            misses = missInfo.group(3)

        return [
            globalRank,
            globalMax,
            countryRank,
            countryMax, 
            accuracy,
            misses,
            nameInfo,
            avatarInfo
        ]
